#!/usr/bin/python3

import sys
import os
import cv2
import numpy as np

def ProcessFile(input, output):
    # 파일 읽기
    img = cv2.imread(input)
    if img is None:
        print(f"Error: Unable to read image {input}")
        return

    # 블러 적용
    blurred = cv2.blur(img, (20, 20))

    # 그레이스케일 변환
    imgray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # 이진화 (Thresholding)
    _, threshed = cv2.threshold(imgray, 120, 255, cv2.THRESH_BINARY)

    # 외곽선 찾기
    cnts = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if not cnts:
        print(f"Error: No contours found in {input}")
        return

    # 면적 기준으로 정렬
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    if len(cnts) < 2:
        print(f"Error: Not enough contours found in {input}")
        return

    cnt = cnts[1]  # 두 번째로 큰 윤곽선 사용

    # 윤곽선 근사화
    arclen = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * arclen, True)

    # 사각형 외곽선 검출
    canvas = np.zeros_like(threshed)
    cv2.drawContours(canvas, [cnt], -1, (255, 0, 0), 5, cv2.LINE_AA)
    cv2.drawContours(canvas, [approx], -1, (0, 0, 255), 5, cv2.LINE_AA)

    # 최소 영역 사각형 찾기
    rect = cv2.minAreaRect(cnts[0])
    _, _, angle = rect

    # 회전 각도 조정
    if angle > 45:
        angle -= 90

    # 중심 좌표 계산
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)

    # 회전 변환 적용
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)

    # 다시 그레이스케일 변환
    imgray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

    # 다시 이진화 적용
    _, threshed = cv2.threshold(imgray, 150, 255, cv2.THRESH_BINARY)

    # 외곽선 다시 찾기
    cnts = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    if not cnts:
        print(f"Error: No valid contours found after rotation in {input}")
        return

    # 바운딩 박스 계산
    x, y, w, h = cv2.boundingRect(cnts[0])

    # 안전한 ROI 범위 계산
    x1, y1 = max(0, x - 10), max(0, y - 10)
    x2, y2 = min(rotated.shape[1], x + w + 20), min(rotated.shape[0], y + h + 20)
    ROI = rotated[y1:y2, x1:x2]

    # 결과 저장
    cv2.imwrite(output, ROI)
    print(f"Processed {input} -> {output}")
    return ROI

