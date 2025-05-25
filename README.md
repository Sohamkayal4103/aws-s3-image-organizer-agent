# S3 Photo Organizer Agent

An AI-powered AWS agent that automatically classifies and sorts your S3 photos into labeled folders using Amazon Rekognition.

---

## 🚀 Features

* **Automated Sorting**: Scans root-level images in your S3 bucket and organizes them into folders based on detected labels.
* **Amazon Rekognition**: Uses AWS Rekognition to perceive and classify image content.
* **Fuzzy Mapping**: Consolidates granular labels into broad categories (e.g., “Breadsticks” → `Food`).
* **Idempotent**: Skips files already in the correct folder to prevent redundant operations.
* **Lightweight**: Zero dependencies beyond `boto3` and the AWS CLI.

---

## 🔧 Prerequisites

* **Python 3.9+**
* **AWS CLI** configured with an IAM user that has **S3** and **Rekognition** permissions:

  ```bash
  aws configure
  ```
* **boto3** Python SDK:

  ```bash
  pip install boto3
  ```

---

## ⚙️ Setup & Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/s3-photo-organizer-agent.git
   cd s3-photo-organizer-agent
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install boto3
   ```

3. **Run the organizer script**

   ```bash
   python organize_photos.py <your-s3-bucket-name>
   ```

4. **Verify the result**

   ```bash
   aws s3 ls s3://<your-s3-bucket-name>/ --recursive
   ```

---

## 📝 Configuration

* **`organize_photos.py`**:

  * Adjust **`IMAGE_EXTS`** to support additional file extensions.
  * Modify the Rekognition confidence thresholds (`max_labels`, `min_conf`) as needed.

* **`categorize.py`**:
  * Customize the **fuzzy category mapping** by editing `CATEGORY_KEYWORDS` and `map_to_category()`.

---
