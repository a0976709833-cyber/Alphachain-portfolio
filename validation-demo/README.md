# Evidence Validation Demo｜證據資料驗證示範

> **Portfolio demonstration / 求職作品展示**  
> 這是依據 AlphaChain 中「資料模型、必要欄位與基本一致性檢查」等公開可說明概念，**重新撰寫的簡化、獨立示範**。不是 AlphaChain 正式產品程式碼，也不包含真實研究資料。

## 這個範例做什麼？

以 Python 與 Pydantic v2（資料模型驗證工具），檢查一筆**虛構的**供應鏈證據紀錄：

- 必填文字不能是空白。
- 來源公司與目標公司不能相同。
- 來源文件日期不能晚於資料擷取日期。
- `stance`（證據立場）只能是 `supporting` 或 `counter`。
- `source_date` 可以是未知（`None`），但 `retrieved_at` 必填。

錯誤資料會產生驗證錯誤，而不是默默進入後續流程。

> **限制：** 通過資料驗證，不等於文件真實、供應鏈關係成立，或因果推論正確。此範例只示範資料結構與邏輯一致性檢查。

## 如何執行

需要 Python 3.10 以上。在終端機切換至本資料夾（`validation-demo/`），依序執行：

```bash
python -m pip install -r requirements.txt
python evidence_validation.py
python -m pytest -q
```

執行示範程式會印出兩行 `PASS`，分別代表合理資料被接受、相同公司關係被拒絕。自動化測試應顯示 **10 passed**。

## 檔案

| 檔案 | 用途 |
| --- | --- |
| `evidence_validation.py` | Pydantic 模型與虛構資料示範 |
| `test_evidence_validation.py` | 正常與異常輸入測試 |
| `requirements.txt` | 執行與測試所需依賴 |

## 展示目的與開發說明

本範例由 AI 協助編寫及執行驗證，用於展示 AlphaChain 開發過程接觸的技術概念；**不宣稱求職者獨立撰寫全部程式碼**。面試時應以自己實際理解、能操作與能解釋的部分說明。建議自行執行、修改與重跑測試後再分享。

公開範例使用完全虛構的公司 ID 與文件名稱，不含主專案原始碼、Git 歷史、API 金鑰或私有研究資料。
