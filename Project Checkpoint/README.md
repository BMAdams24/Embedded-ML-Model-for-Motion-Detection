# Final Project - Embedded ML Model for Motion Detection
---
#### **Partner:** Mica Helou 
#### **Raspberry Pi Number:** 975822
---
### **File Content:**
| File | Description |
|------|-------------|
| [`fall_detect_nn_Xnp_student (4).ipynb`] | Original unoptimized model for training and evaluation |
| [`EMB_Model_MH_BA_OPTIMIZED.ipynb`] | Optimized model notebook |
| [`EMB_Model_MH_BA_OPTIMIZED.tflite`] | TFLite optimized model |
| [`predict.py`] | Python script for running inference in Raspberry Pi |

---
## **Optimizations:**
### Accuracy Improvements Optimizations:
| Change | Original | Optimized | Strategy |
|--------|----------|-----------|--------|
| **Epochs** | 15 | 100 | Allowed model to better converge with sufficient training iterations |
| **Architecture** | 2 dense layers: 64 → 32 → output | 3 dense layers: 128 → 64 → 32 → output with Dropout(0.3) | Increased model capacity and added regularization |
| **Window Size** | 50 | 10 | Reduced input feature size, improving speed without hurting accuracy |
| **Activation Function** | ReLU | ReLU + Softmax output | Ensured probability output and non-linearity |
| **Input Normalization** | None | StandardScaler applied | Ensured faster and more stable convergence |
| **Loss Function** | BinaryCrossentropy | SparseCategoricalCrossentropy | Better suited for multi-class fall classification |
| **Data Augmentation** | None | Added Gaussian noise to features | Increased model robustness and generalization |

### Model Compression and Speed Optimizations:
| Change | Original | Optimized | Strategy |
|--------|----------|-----------|--------|
| **Quantization** | None | Post-training dynamic + int8 quantization | Reduced model size and RAM usage |
| **Model Size** | 164 KB | **54.3 KB** | Enabled edge device compatibility |
| **Inference Time (Raspberry Pi)** | 0.04905328753442 s | **0.044351577758 s** | Reduced inference |
| **Layer Reduction** | Fully connected layers with many neurons | Smaller layer sizes (128 → 64 → 32) | Balanced performance with computation efficiency |
| **Pruning** | Not used | Prunning | Reduced number of trainable parameters, shrinking size and accelerating inference |
---
## **Model Performance:**
| Metric | Original Model | Optimized Model |
|--------|----------------|-----------------|
| **Accuracy** | 92% | 95% |
| **Model Size** | 164 KB | **54.3 KB** |
| **Inference Time** | 0.04905328753442 s | **0.044351577758 s** |
