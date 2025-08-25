class SystemService:
    
    @staticmethod
    def get_status():
        return {
            "status": "ok",
            "model_loaded": True
        }
        

system_service = SystemService()