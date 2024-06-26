import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import CSVLogger

# Tải dữ liệu
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Tiền xử lý dữ liệu
X_train = X_train.reshape((X_train.shape[0], 28, 28, 1))
X_test = X_test.reshape((X_test.shape[0], 28, 28, 1))
X_train, X_test = X_train / 255.0, X_test / 255.0
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Khởi tạo mô hình
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

# Compile mô hình
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Đường dẫn lưu file log
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file_path = os.path.join(log_dir, "training_log.csv")

# Khởi tạo CSVLogger callback
csv_logger = CSVLogger(log_file_path, append=False)

# Huấn luyện mô hình
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=200, callbacks=[csv_logger])

# Lưu mô hình
model.save('mnist_model.h5')