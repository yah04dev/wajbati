# Wajbati AI-Powered Dietary Assessment and Calorie Tracking Platform

An intelligent web application for personalized dietary assessment, food recognition, and AI-assisted calorie tracking using deep learning and computer vision.

---

# Overview

This project is a graduation thesis developed at the University of Abdelhamid Mehri Constantine 2.

The platform combines artificial intelligence, computer vision, and nutritional tracking technologies to help users monitor their dietary habits through automated food recognition and calorie estimation.

The system allows users to upload food images, automatically detect food items, estimate nutritional values, track meal history, and interact with nutritionists through an integrated web platform.

---

# Main Features

## User Features

- User registration and authentication
- Personalized profile and fitness goals
- Food image upload
- AI-powered food recognition
- Automatic calorie estimation
- Meal history tracking
- Progress monitoring dashboard
- Nutritionist consultation booking
- Premium subscription simulation

## Nutritionist Features

- Nutritionist dashboard
- Client management system
- Consultation management
- Personalized meal recommendations
- Progress monitoring

## AI Features

- Multi-food detection
- Instance segmentation
- Real-time inference
- Portion estimation
- Nutritional value estimation
- YOLOv8s-seg based segmentation model

---

# AI Model

The project uses YOLOv8s-seg for food instance segmentation and calorie estimation.

## Dataset

The model was trained using the FoodInsSeg dataset.

Dataset characteristics:

- 7,118 images
- 103 food classes
- COCO segmentation annotations
- Real-world food images

---

# Model Variants

| Model | Classes | mAP@0.5 | Precision | Recall |
|---|---|---|---|---|
| YOLOv8s-seg Model 1 | 103 | 0.1845 | 0.2988 | 0.2302 |
| YOLOv8s-seg Model 2 (Fine-tuned) | 26 | 0.3180 | 0.3900 | 0.3500 |

---

# AI Technologies

- Python
- PyTorch
- Ultralytics YOLOv8
- OpenCV
- NumPy
- Matplotlib

---

# System Architecture

The application follows a client-server architecture composed of several layers.

## Backend

- Flask
- SQLite
- REST-style routing

## Frontend

- HTML
- CSS
- Jinja2 Templates
- JavaScript

## AI Module

- YOLOv8s-seg
- ONNX export support

## Additional Integrations

- Jitsi Meet for online meetings
- Chargily payment gateway simulation
- JSON nutrition database

---

# Project Structure

```bash
project/
│
├── app.py
├── db.db
├── nutrition_db.json
│
├── models/
│   ├── best_yolov8s.pt
│   └── best_yolov8s.onnx
│
├── static/
├── templates/
├── uploads/
│
├── train/
├── val/
│
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

---

# Deployment

The application can be deployed using Gunicorn for production environments.

Example:

```bash
gunicorn app:app
```

Recommended deployment stack:

- Gunicorn
- Nginx
- Ubuntu Server

---

# Experimental Results

The second fine-tuned model significantly improved segmentation performance by:

- Reducing class complexity
- Applying transfer learning
- Fine-tuning from food-domain weights

## Improvements Achieved

- Approximately 72% improvement in mAP@0.5
- Better precision and recall
- Faster convergence during training
- Reduced background misclassification

---

# Technologies Used

## Backend

- Flask
- SQLite
- Werkzeug

## Artificial Intelligence

- YOLOv8s-seg
- PyTorch
- OpenCV

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2

## Deployment and Tools

- Gunicorn
- Kaggle GPU Environment
- ONNX

---

# Database

The system uses SQLite for relational data storage.

Main tables include:

- Client
- Nutritionist
- Consultation
- Progress
- Meal
- Admin

Nutritional information is stored separately in a JSON nutrition database.

---

# AI Workflow

The AI pipeline follows several sequential stages:

1. User uploads a food image
2. Image preprocessing
3. Food detection using YOLOv8s-seg
4. Instance segmentation
5. Portion estimation
6. Nutritional lookup
7. Calorie calculation
8. Dashboard visualization
9. Data storage

---

# Future Improvements

Potential future enhancements include:

- Real payment integration
- Mobile application support
- Larger food datasets
- Improved portion estimation
- Personalized AI recommendations
- Cloud deployment
- Arabic language support
- Real-time mobile inference optimization

---

# Thesis Information

Bachelor Dissertation

Faculty of New Technologies of Information and Communication (NTIC)  
University of Abdelhamid Mehri Constantine 2

## Authors

- Yahia Abdeljallil Benamrouche
- Hamza Abdarrahmane Bensmira

## Supervisor

- Dr. Bechinia Hadjer

---

# Citation

```bibtex
@misc{ai_calorie_tracking_2026,
  title={AI-Powered Dietary Assessment and Calorie Tracking},
    author={Benamrouche, Yahia Abdeljallil and Bensmira, Hamza Abdarrahmane},
      year={2026},
        school={University of Constantine 2}
        }
        ```

        ---

        # License

        This project was developed for academic and educational purposes.

        ---

        # Acknowledgments

        Special thanks to:

        - Dr. Bechinia Hadjer
        - University of Constantine 2
        - Faculty of NTIC
        - Open-source AI community
        - Ultralytics YOLO team

        ---

        # Contact

        For questions or collaboration opportunities, feel free to open an issue or contact the authors through GitHub.# AI-Powered Dietary Assessment and Calorie Tracking

        An intelligent web application for personalized dietary assessment, food recognition, and AI-assisted calorie tracking using deep learning and computer vision.

        ---

        # Overview

        This project is a graduation thesis developed at the University of Abdelhamid Mehri Constantine 2.

        The platform combines artificial intelligence, computer vision, and nutritional tracking technologies to help users monitor their dietary habits through automated food recognition and calorie estimation.

        The system allows users to upload food images, automatically detect food items, estimate nutritional values, track meal history, and interact with nutritionists through an integrated web platform.

        ---

        # Main Features

        ## User Features

        - User registration and authentication
        - Personalized profile and fitness goals
        - Food image upload
        - AI-powered food recognition
        - Automatic calorie estimation
        - Meal history tracking
        - Progress monitoring dashboard
        - Nutritionist consultation booking
        - Premium subscription simulation

        ## Nutritionist Features

        - Nutritionist dashboard
        - Client management system
        - Consultation management
        - Personalized meal recommendations
        - Progress monitoring

        ## AI Features

        - Multi-food detection
        - Instance segmentation
        - Real-time inference
        - Portion estimation
        - Nutritional value estimation
        - YOLOv8s-seg based segmentation model

        ---

        # AI Model

        The project uses YOLOv8s-seg for food instance segmentation and calorie estimation.

        ## Dataset

        The model was trained using the FoodInsSeg dataset.

        Dataset characteristics:

        - 7,118 images
        - 103 food classes
        - COCO segmentation annotations
        - Real-world food images

        ---

        # Model Variants

        | Model | Classes | mAP@0.5 | Precision | Recall |
        |---|---|---|---|---|
        | YOLOv8s-seg Model 1 | 103 | 0.1845 | 0.2988 | 0.2302 |
        | YOLOv8s-seg Model 2 (Fine-tuned) | 26 | 0.3180 | 0.3900 | 0.3500 |

        ---

        # AI Technologies

        - Python
        - PyTorch
        - Ultralytics YOLOv8
        - OpenCV
        - NumPy
        - Matplotlib

        ---

        # System Architecture

        The application follows a client-server architecture composed of several layers.

        ## Backend

        - Flask
        - SQLite
        - REST-style routing

        ## Frontend

        - HTML
        - CSS
        - Jinja2 Templates
        - JavaScript

        ## AI Module

        - YOLOv8s-seg
        - ONNX export support

        ## Additional Integrations

        - Jitsi Meet for online meetings
        - Chargily payment gateway simulation
        - JSON nutrition database

        ---

        # Project Structure

        ```bash
        project/
        │
        ├── app.py
        ├── db.db
        ├── nutrition_db.json
        │
        ├── models/
        │   ├── best_yolov8s.pt
        │   └── best_yolov8s.onnx
        │
        ├── static/
        ├── templates/
        ├── uploads/
        │
        ├── train/
        ├── val/
        │
        └── README.md
        ```

        ---

        # Installation

        ## 1. Clone the Repository

        ```bash
        git clone https://github.com/your-username/your-repository.git
        cd your-repository
        ```

        ---

        ## 2. Create a Virtual Environment

        ### Windows

        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

        ### Linux / macOS

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

        ---

        ## 3. Install Dependencies

        ```bash
        pip install -r requirements.txt
        ```

        ---

        ## 4. Run the Application

        ```bash
        python app.py
        ```

        ---

        # Deployment

        The application can be deployed using Gunicorn for production environments.

        Example:

        ```bash
        gunicorn app:app
        ```

        Recommended deployment stack:

        - Gunicorn
        - Nginx
        - Ubuntu Server

        ---

        # Experimental Results

        The second fine-tuned model significantly improved segmentation performance by:

        - Reducing class complexity
        - Applying transfer learning
        - Fine-tuning from food-domain weights

        ## Improvements Achieved

        - Approximately 72% improvement in mAP@0.5
        - Better precision and recall
        - Faster convergence during training
        - Reduced background misclassification

        ---

        # Technologies Used

        ## Backend

        - Flask
        - SQLite
        - Werkzeug

        ## Artificial Intelligence

        - YOLOv8s-seg
        - PyTorch
        - OpenCV

        ## Frontend

        - HTML5
        - CSS3
        - JavaScript
        - Jinja2

        ## Deployment and Tools

        - Gunicorn
        - Kaggle GPU Environment
        - ONNX

        ---

        # Database

        The system uses SQLite for relational data storage.

        Main tables include:

        - Client
        - Nutritionist
        - Consultation
        - Progress
        - Meal
        - Admin

        Nutritional information is stored separately in a JSON nutrition database.

        ---

        # AI Workflow

        The AI pipeline follows several sequential stages:

        1. User uploads a food image
        2. Image preprocessing
        3. Food detection using YOLOv8s-seg
        4. Instance segmentation
        5. Portion estimation
        6. Nutritional lookup
        7. Calorie calculation
        8. Dashboard visualization
        9. Data storage

        ---

        # Future Improvements

        Potential future enhancements include:

        - Real payment integration
        - Mobile application support
        - Larger food datasets
        - Improved portion estimation
        - Personalized AI recommendations
        - Cloud deployment
        - Arabic language support
        - Real-time mobile inference optimization

        ---

        # Thesis Information

        Bachelor Dissertation

        Faculty of New Technologies of Information and Communication (NTIC)  
        University of Abdelhamid Mehri Constantine 2

        ## Authors

        - Yahia Abdeljallil Benamrouche
        - Hamza Abdarrahmane Bensmira

        ## Supervisor

        - Dr. Bechinia Hadjer

        ---

        # Citation

        ```bibtex
        @misc{ai_calorie_tracking_2026,
          title={AI-Powered Dietary Assessment and Calorie Tracking},
            author={Benamrouche, Yahia Abdeljallil and Bensmira, Hamza Abdarrahmane},
              year={2026},
                school={University of Constantine 2}
                }
                ```

                ---

                # License

                This project was developed for academic and educational purposes.

                ---

                # Acknowledgments

                Special thanks to:

                - Dr. Bechinia Hadjer
                - University of Constantine 2
                - Faculty of NTIC
                - Open-source AI community
                - Ultralytics YOLO team

                ---

                # Contact

                For questions or collaboration opportunities, feel free to open an issue or contact the authors through GitHub.
