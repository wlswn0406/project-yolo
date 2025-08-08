class YOLOEngine:
    def __init__(self, config_path=None):
        self.config = self.load_config(config_path)
        self.model = None
        self.experiment_tracker = ExperimentTracker()
    
    def full_pipeline(self):
        """전체 파이프라인 실행"""
        self.prepare_data()
        model = self.train_model()
        metrics = self.evaluate_model(model)
        self.save_experiment_results(metrics)
        return model, metrics
    
    def auto_tune(self, param_ranges):
        """하이퍼파라미터 자동 튜닝"""
        best_score = 0
        best_params = None
        
        for params in self.generate_param_combinations(param_ranges):
            model = self.train_model(**params)
            score = self.evaluate_model(model)
            if score > best_score:
                best_score = score
                best_params = params
        
        return best_params
    
    def serve_model(self, host, port, api_type="REST"):
        """모델 서빙"""
        if api_type == "REST":
            self.create_rest_api(host, port)
        elif api_type == "gRPC":
            self.create_grpc_server(host, port)            # 1. 이미지 빌드
            docker build -t yolo-engine .
            
            # 2. 기본 실행 (훈련)
            docker-compose up yolo-engine
            
            # 3. API 서버 실행
            docker-compose up yolo-api
            
            # 4. GPU 사용 (NVIDIA Docker 필요)
            docker-compose up yolo-gpu
            
            # 5. 개별 명령 실행
            docker run -v $(pwd)/data:/workspace/data -v $(pwd)/outputs:/workspace/outputs yolo-engine python examples/basic_training.py