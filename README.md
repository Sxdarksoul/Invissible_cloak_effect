# Invissible_cloak_effect
🧙‍♂️ Invisible Cloak Effect (OpenCV + Python + Tkinter)

A fun Harry Potter–style Invisible Cloak effect created using Python, OpenCV, NumPy, and a clean Tkinter GUI.
The project detects a specific cloth color (red/blue) and replaces it with the background, making the cloth — and the person behind it — appear invisible.

This project demonstrates computer vision, color masking, GUI design, and real-time video processing in Python.

🎥 Demo

(demo.png)


🚀 Features

🖥 Modern Tkinter GUI (Black & White theme)

🎛 Start / Stop buttons

🎨 Select cloak color (Red / Blue)

🔊 Beep sound when background is ready

🎥 Live camera preview inside the GUI (no OpenCV pop-ups)

🪄 Background replacement for invisibility

💡 Beginner-friendly and well-structured code

📦 Requirements

Install all required packages using:

pip install -r requirements.txt


Dependencies include:

opencv-python

numpy

Pillow

These are already listed in your requirements.txt.

▶️ How to Run

Clone the repository:

git clone https://github.com/Sxdarksoul/Invissible_cloak_effect.git


Navigate to the folder:

cd Invissible_cloak_effect


Run the application:

python invisible_cloak.py


(or whichever file you uploaded — update filename accordingly)

🧩 How It Works

The app captures several frames of the background.

It detects the cloak color using HSV color space masking.

The cloak area is replaced with the saved background.

Real-time camera feed is displayed inside the GUI window.

📂 Project Structure
Invissible_cloak_effect/
│
├── invisible_cloak.py (or main GUI file)
├── requirements.txt
└── README.md


If you add folders later (like src/ or assets/), update this section accordingly.

💡 Future Improvements

Some ideas to expand the project later:

Add a progress bar during background capture

Add a record video feature

Add multiple color detection

Add noise reduction filters

Add seamless blending with OpenCV’s seamlessClone

📝 License

This project is free to use and modify.

👤 Author

Sxdarksoul
Feel free to connect or star the repo ⭐
