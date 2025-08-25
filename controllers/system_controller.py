from services.system_service import system_service

class SystemController:
    
    @staticmethod
    def get_status():
        return system_service.get_status()
    
    
system_controller = SystemController()