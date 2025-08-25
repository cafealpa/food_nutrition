import cv2
import numpy as np

def crop_image_by_coordinates(image_path, x1, y1, x2, y2, output_path=None):
    """
    좌표를 사용해서 이미지를 크롭하는 함수
    
    Parameters:
    image_path (str): 입력 이미지 파일 경로
    x1, y1 (int): 크롭 영역의 시작점 좌표 (왼쪽 위)
    x2, y2 (int): 크롭 영역의 끝점 좌표 (오른쪽 아래)
    output_path (str, optional): 출력 파일 경로 (None이면 저장하지 않음)
    
    Returns:
    cropped_image: 크롭된 이미지 배열
    """
    # 이미지 읽기
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"이미지를 불러올 수 없습니다: {image_path}")
        return None
    
    # 이미지 크기 확인
    height, width = image.shape[:2]
    print(f"원본 이미지 크기: {width} x {height}")
    
    # 좌표 유효성 검사
    x1 = max(0, min(x1, width))
    y1 = max(0, min(y1, height))
    x2 = max(0, min(x2, width))
    y2 = max(0, min(y2, height))
    
    # 좌표 순서 확인 (x1 < x2, y1 < y2가 되도록)
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    
    print(f"크롭 좌표: ({x1}, {y1}) to ({x2}, {y2})")
    
    # 이미지 크롭 (numpy 슬라이싱 사용)
    cropped_image = image[y1:y2, x1:x2]
    
    print(f"크롭된 이미지 크기: {cropped_image.shape[1]} x {cropped_image.shape[0]}")
    
    # 결과 저장 (선택사항)
    if output_path:
        cv2.imwrite(output_path, cropped_image)
        print(f"크롭된 이미지가 저장되었습니다: {output_path}")
    
    return cropped_image

# 사용 예시
if __name__ == "__main__":
    # 방법 1: 직접 좌표 지정
    image_path = "Img_000_0001.jpg"  # 입력 이미지 경로
    output_path = "cropped_Img_000_0001.jpg"  # 출력 이미지 경로
    
    # 좌표로 크롭 (x1, y1, x2, y2)
    cropped_img = crop_image_by_coordinates(
        image_path=image_path,
        x1=45,    # 시작 x 좌표
        y1=76,     # 시작 y 좌표
        x2=538,    # 끝 x 좌표
        y2=404,    # 끝 y 좌표
        output_path=output_path
    )