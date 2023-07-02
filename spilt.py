import os
import shutil
import random

def split_data_folder(input_folder, train_folder, val_folder, split_ratio):
    # 創建TrainingSet和ValidationSet資料夾（如果不存在）
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # 獲取所有檔案名稱，並根據副檔名進行分組
    files = {}
    for filename in os.listdir(input_folder):
        basename, ext = os.path.splitext(filename)
        if basename not in files:
            files[basename] = []
        files[basename].append(filename)

    # 隨機打亂每個分組的檔案順序
    for group in files.values():
        random.shuffle(group)

    # 決定要分配到TrainingSet和ValidationSet的檔案數量
    train_count = int(len(files) * split_ratio)
    val_count = len(files) - train_count

    # 從每個分組中拆分檔案到TrainingSet
    count = 0
    for group in files.values():
        if count < train_count:
            for filename in group:
                source_path = os.path.join(input_folder, filename)
                target_path = os.path.join(train_folder, filename)
                shutil.copy(source_path, target_path)
                count += 1

    # 將剩餘的檔案拆分到ValidationSet
    for group in files.values():
        if count < len(files):
            for filename in group:
                source_path = os.path.join(input_folder, filename)
                target_path = os.path.join(val_folder, filename)
                shutil.copy(source_path, target_path)
                count += 1

    print("資料夾拆分完成！")

# 指定輸入資料夾路徑、TrainingSet資料夾路徑、ValidationSet資料夾路徑和拆分比例
input_folder = "C:/Users//salasrew//Desktop//EMBA//pictures0623"

train_folder = "C://Users//salasrew//Desktop//EMBA//train_folder"
val_folder = "C://Users//salasrew//Desktop//EMBA//val_folder"

split_ratio = 0.8

# 呼叫函式執行拆分
split_data_folder(input_folder, train_folder, val_folder, split_ratio)
