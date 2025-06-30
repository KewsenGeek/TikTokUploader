#!/usr/bin/env python
"""
Isolated Cookie Robot script for subprocess execution
Completely isolated from Django async context
"""
import asyncio
import json
import sys
import os
import logging
import platform

def log_message(message):
    """Simple logging function"""
    print(f"[ISOLATED] {message}", file=sys.stderr)

async def run_cookie_robot_isolated(params):
    try:
        profile_id = params['profile_id']
        urls = params['urls']
        headless = params['headless']
        imageless = params['imageless']
        duration = params['duration']
        api_key = params['api_key']
        local_api_base = params['local_api_base']
        
        log_message(f"Starting Cookie Robot for profile {profile_id}")
        log_message(f"URLs: {len(urls)}, Duration: {duration}s")
        
        # Добавляем корневую директорию проекта в sys.path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        log_message(f"Added to sys.path: {project_root}")
        
        # Альтернативный способ - ищем manage.py в родительских директориях
        search_dir = current_dir
        for _ in range(5):  # Ограничиваем поиск 5 уровнями вверх
            if os.path.exists(os.path.join(search_dir, 'manage.py')):
                if search_dir not in sys.path:
                    sys.path.insert(0, search_dir)
                log_message(f"Found manage.py, added to sys.path: {search_dir}")
                break
            search_dir = os.path.dirname(search_dir)
        
        # Также добавляем текущую рабочую директорию
        cwd = os.getcwd()
        if cwd not in sys.path:
            sys.path.insert(0, cwd)
        log_message(f"Added current working directory to sys.path: {cwd}")
        
        # Импортируем DolphinAnty в изолированном контексте
        try:
            from bot.src.instagram_uploader.dolphin_anty import DolphinAnty
        except ImportError as e:
            log_message(f"Failed to import DolphinAnty: {e}")
            log_message(f"Current sys.path: {sys.path}")
            raise ImportError(f"Cannot import DolphinAnty: {e}")
        
        log_message("Successfully imported DolphinAnty")
        
        # Создаем экземпляр DolphinAnty
        dolphin = DolphinAnty(api_key=api_key, local_api_base=local_api_base)
        
        # Запускаем async метод напрямую (теперь мы в изолированном контексте)
        result = await dolphin.run_cookie_robot(
            profile_id=profile_id,
            urls=urls,
            headless=headless,
            imageless=imageless,
            duration=duration,
            task_logger=lambda msg: log_message(msg)
        )
        
        return result
        
    except Exception as e:
        log_message(f"Error in isolated cookie robot: {str(e)}")
        return {"success": False, "error": f"Isolated execution error: {str(e)}"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No parameters file provided"}))
        sys.exit(1)
    
    params_file = sys.argv[1]
    
    try:
        # Читаем параметры из файла
        with open(params_file, 'r') as f:
            params = json.load(f)
        
        # Windows-specific: устанавливаем правильный event loop policy
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Создаем новый event loop в изолированном процессе
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Выполняем Cookie Robot
            result = loop.run_until_complete(run_cookie_robot_isolated(params))
            
            # Выводим результат в stdout как JSON
            print(json.dumps(result))
            
        finally:
            loop.close()
            
    except Exception as e:
        error_result = {"success": False, "error": f"Main execution error: {str(e)}"}
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()
