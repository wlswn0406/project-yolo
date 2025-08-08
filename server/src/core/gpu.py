def test_pytorch_operations():
    """PyTorch 기본 동작 테스트"""
    try:
        # CUDA 사용 가능 여부 체크
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"{Fore.CYAN}\n=== PyTorch 테스트 시작 ===")
        print(f"{Fore.YELLOW}사용 중인 장치:", device)
        
        # 간단한 텐서 연산 테스트
        x = torch.rand(2, 3, device=device)
        y = torch.rand(3, 2, device=device)
        result = torch.mm(x, y)
        
        # 결과 검증
        assert result.shape == (2, 2), "행렬 곱셈 결과 차원 불일치"
        print(f"{Fore.GREEN}✓ 기본 텐서 연산 테스트 통과")
        
        # CUDA 추가 정보 출력
        if device.type == 'cuda':
            print(f"{Fore.YELLOW}CUDA 장치 이름:", torch.cuda.get_device_name(0))
            print(f"할당된 메모리:", round(torch.cuda.memory_allocated(0)/1024**3, 1), "GB")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}✗ 테스트 실패:", str(e))
        return False
    finally:
        print(f"{Fore.CYAN}=== 테스트 종료 ===\n")
