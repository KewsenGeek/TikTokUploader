from __future__ import annotations
import json
from typing import Any, Dict, List
from django.conf import settings
from django.http import JsonResponse, FileResponse, HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from uploader.models import (
    BulkUploadTask, BulkUploadAccount, BulkVideo,
    BulkLoginTask, BulkLoginAccount,
    WarmupTask, WarmupTaskAccount,
    AvatarChangeTask, AvatarChangeTaskAccount, AvatarImage,
    BioLinkChangeTask, BioLinkChangeTaskAccount,
    FollowTask, FollowTaskAccount, FollowTarget,
)


def _auth_ok(request) -> bool:
    auth = request.headers.get("Authorization") or ""
    token = settings.WORKER_API_TOKEN
    if not token:
        return False
    if not auth.startswith("Bearer "):
        return False
    return auth.split(" ", 1)[1] == token


def _forbidden() -> HttpResponse:
    return HttpResponseForbidden(JsonResponse({"detail": "Forbidden"}).content, content_type="application/json")


# ===== Bulk Upload =====

@require_GET
@csrf_exempt
def bulk_task_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(BulkUploadTask, id=task_id)
    accounts_payload = []
    for at in task.accounts.select_related("account", "proxy").all():
        acc = at.account
        accounts_payload.append({
            "account_task_id": at.id,
            "account": acc.to_dict(),
        })
    videos_payload = []
    for v in task.videos.order_by("order", "id").all():
        title_val = getattr(v, 'title_data', None).title if getattr(v, 'title_data', None) else None
        videos_payload.append({
            "id": v.id,
            "order": v.order,
            "title": title_val,
            "location": v.location or "",
            "mentions": v.mentions or "",
            "url": None,
        })
    payload = {
        "id": task.id,
        "default_location": task.default_location or "",
        "default_mentions": task.default_mentions or "",
        "accounts": accounts_payload,
        "videos": videos_payload,
    }
    return JsonResponse(payload)

@require_GET
@csrf_exempt
def media_download(request, video_id: int):
    if not _auth_ok(request):
        return _forbidden()
    v = get_object_or_404(BulkVideo, id=video_id)
    if not v.video_file:
        raise Http404("Video file not found")
    return FileResponse(v.video_file.open("rb"), as_attachment=True, filename=v.video_file.name.split("/")[-1])

@require_POST
@csrf_exempt
def bulk_task_status(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(BulkUploadTask, id=task_id)
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    status_val = data.get("status")
    log = data.get("log")
    log_append = data.get("log_append")
    if status_val:
        task.status = status_val
    if log:
        task.log = (task.log or "") + log + "\n"
    if log_append:
        task.log = (task.log or "") + log_append + "\n"
    task.save(update_fields=['status','log','updated_at'])
    return JsonResponse({"ok": True, "status": task.status})

@require_POST
@csrf_exempt
def bulk_account_status(request, account_task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    at = get_object_or_404(BulkUploadAccount, id=account_task_id)
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    status_val = data.get("status")
    log_append = data.get("log_append")
    if status_val:
        at.status = status_val
    if log_append:
        at.log = (at.log or "") + log_append + "\n"
    at.save(update_fields=['status','log','updated_at'])
    return JsonResponse({"ok": True, "status": at.status})

@require_POST
@csrf_exempt
def bulk_account_counters(request, account_task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    at = get_object_or_404(BulkUploadAccount, id=account_task_id)
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    at.uploaded_success_count = (at.uploaded_success_count or 0) + int(data.get('success', 0) or 0)
    at.uploaded_failed_count = (at.uploaded_failed_count or 0) + int(data.get('failed', 0) or 0)
    at.save(update_fields=['uploaded_success_count','uploaded_failed_count','updated_at'])
    return JsonResponse({
        "ok": True,
        "uploaded_success_count": at.uploaded_success_count,
        "uploaded_failed_count": at.uploaded_failed_count,
    })


# ===== Placeholders for other aggregates (return minimal structure until full mapping is needed) =====

@require_GET
@csrf_exempt
def bulk_login_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(BulkLoginTask, id=task_id)
    accounts = [
        {"account_task_id": at.id, "account": at.account.to_dict()}
        for at in task.accounts.select_related("account","proxy").all()
    ]
    return JsonResponse({"id": task.id, "accounts": accounts})

@require_GET
@csrf_exempt
def warmup_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(WarmupTask, id=task_id)
    accounts = [
        {"account_task_id": at.id, "account": at.account.to_dict()}
        for at in task.accounts.select_related("account","proxy").all()
    ]
    actions = {
        "feed_scroll_min_count": task.feed_scroll_min_count,
        "feed_scroll_max_count": task.feed_scroll_max_count,
        "like_min_count": task.like_min_count,
        "like_max_count": task.like_max_count,
        "view_stories_min_count": task.view_stories_min_count,
        "view_stories_max_count": task.view_stories_max_count,
        "follow_min_count": task.follow_min_count,
        "follow_max_count": task.follow_max_count,
    }
    return JsonResponse({"id": task.id, "actions": actions, "accounts": accounts})

@require_GET
@csrf_exempt
def avatar_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(AvatarChangeTask, id=task_id)
    accounts = [
        {"account_task_id": at.id, "account": at.account.to_dict()}
        for at in task.accounts.select_related("account","proxy").all()
    ]
    images = [
        {"id": img.id, "order": img.order, "url": None}
        for img in task.images.order_by('order','id').all()
    ]
    return JsonResponse({"id": task.id, "strategy": task.strategy, "accounts": accounts, "images": images})

@require_GET
@csrf_exempt
def bio_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(BioLinkChangeTask, id=task_id)
    accounts = [
        {"account_task_id": at.id, "account": at.account.to_dict()}
        for at in task.accounts.select_related("account","proxy").all()
    ]
    return JsonResponse({"id": task.id, "link_url": task.link_url, "accounts": accounts})

@require_GET
@csrf_exempt
def follow_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(FollowTask, id=task_id)
    accounts = [
        {"account_task_id": at.id, "account": at.account.to_dict()}
        for at in task.accounts.select_related("account","proxy").all()
    ]
    targets = [
        {"username": t.username} for t in FollowTarget.objects.filter(category=task.category).all()
    ]
    options = {"follow_min_count": task.follow_min_count, "follow_max_count": task.follow_max_count}
    return JsonResponse({"id": task.id, "accounts": accounts, "targets": targets, "options": options})

@require_GET
@csrf_exempt
def proxy_diag_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(BulkUploadTask, id=task_id)  # или отдельная модель задач для прокси
    accounts = [
        {"account_task_id": at.id, "account": at.account.to_dict()}
        for at in task.accounts.select_related("account","proxy").all()
    ]
    return JsonResponse({"id": task.id, "accounts": accounts})

@require_GET
@csrf_exempt
def media_uniq_aggregate(request, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    task = get_object_or_404(BulkUploadTask, id=task_id)
    videos = [
        {"id": v.id, "url": None}
        for v in task.videos.order_by('order','id').all()
    ]
    return JsonResponse({"id": task.id, "videos": videos})


# ===== Generic status endpoints for other kinds =====

_KIND_TASK_MODEL = {
    'bulk_login': BulkLoginTask,
    'warmup': WarmupTask,
    'avatar': AvatarChangeTask,
    'bio': BioLinkChangeTask,
    'follow': FollowTask,
    'proxy_diag': BulkUploadTask,
    'media_uniq': BulkUploadTask,
}

_KIND_ACCOUNT_MODEL = {
    'bulk_login': BulkLoginAccount,
    'warmup': WarmupTaskAccount,
    'avatar': AvatarChangeTaskAccount,
    'bio': BioLinkChangeTaskAccount,
    'follow': FollowTaskAccount,
    'proxy_diag': BulkUploadAccount,
}


def _get_task_model(kind: str):
    return _KIND_TASK_MODEL.get(kind)


def _get_account_model(kind: str):
    return _KIND_ACCOUNT_MODEL.get(kind)


@require_POST
@csrf_exempt
def generic_task_status(request, kind: str, task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    Model = _get_task_model(kind)
    if not Model:
        return JsonResponse({"detail": "Unknown kind"}, status=400)
    task = get_object_or_404(Model, id=task_id)
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    status_val = data.get("status")
    log = data.get("log")
    log_append = data.get("log_append")
    if hasattr(task, 'status') and status_val:
        task.status = status_val
    if hasattr(task, 'log') and (log or log_append):
        if log:
            task.log = (task.log or "") + log + "\n"
        if log_append:
            task.log = (task.log or "") + log_append + "\n"
    task.save()
    return JsonResponse({"ok": True, "status": getattr(task, 'status', None)})


@require_POST
@csrf_exempt
def generic_account_status(request, kind: str, account_task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    Model = _get_account_model(kind)
    if not Model:
        return JsonResponse({"detail": "Unknown kind"}, status=400)
    at = get_object_or_404(Model, id=account_task_id)
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    status_val = data.get("status")
    log_append = data.get("log_append")
    if hasattr(at, 'status') and status_val:
        at.status = status_val
    if hasattr(at, 'log') and log_append:
        at.log = (at.log or "") + log_append + "\n"
    at.save()
    return JsonResponse({"ok": True, "status": getattr(at, 'status', None)})


@require_POST
@csrf_exempt
def generic_account_counters(request, kind: str, account_task_id: int):
    if not _auth_ok(request):
        return _forbidden()
    Model = _get_account_model(kind)
    if not Model:
        return JsonResponse({"detail": "Unknown kind"}, status=400)
    at = get_object_or_404(Model, id=account_task_id)
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
    except json.JSONDecodeError:
        data = {}
    # Best-effort counter fields if present
    for key in ("success", "failed", "likes", "follows", "viewed"):
        if hasattr(at, key) and key in data:
            try:
                setattr(at, key, (getattr(at, key) or 0) + int(data.get(key) or 0))
            except Exception:
                pass
    at.save()
    return JsonResponse({"ok": True}) 