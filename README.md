### **Project Title:** Project-ITT-Brain-Raspberry-PI-v2

**Description:**

The Project-ITT-Brain-Raspberry-PI-v2 is a Python-based project designed to serve as the central processing unit for a cutting-edge voice and joystick-controlled wheelchair. The system integrates advanced features, including fall detection, real-time image capture, and location tracking. The project is tailored for the Raspberry Pi platform and seamlessly interfaces with an STM32 microcontroller, ensuring a responsive and adaptable user experience.

**Key Features:**

1. **Fall Detection System:**
    - Utilizes sensor data from the STM32 microcontroller to detect potential falls.
    - Initiates real-time image capture through the Raspberry Pi Camera upon fall detection.
    - Gathers precise location information from a connected GPS module.
2. **Multi-Threading:**
    - Employs two threads to independently handle critical functionalities.
    - **Thread 1:** Monitors and processes data from the STM32 microcontroller.
    - **Thread 2:** Listens for voice commands using a speech recognition library.
3. **GPRS Connectivity:**
    - Ensures continuous operation by connecting to the internet through a GPRS module if Wi-Fi is unavailable.
    - Facilitates seamless communication between the wheelchair system and external servers or APIs.
4. **API-REST Integration:**
    - Utilizes the RESTful API architecture to securely transmit fall detection alerts to a web application.
    - Enables real-time display of captured images and location information to keep users and caregivers informed.
5. **Voice Control:**
    - Implements voice control for directional commands (ahead, back, left, right) when the special word is present, the name of the wheelchair ‘Sofia”, and when this mode is selected in the wheelchair.

**Why Multi-Threading:**

- Multi-threading enhances system responsiveness and efficiency.
- Separating tasks into threads allows parallel execution, preventing one task from blocking others.
- Ensures a smooth and real-time response to both fall detection and user commands.

**Why API-REST:**

- API-REST ensures a standardized and scalable communication protocol.
- Facilitates interoperability with web applications and other connected devices.
- Provides a secure and reliable means of transmitting critical information.

**Dependencies:**

- Python
- Raspberry Pi
- STM32 Microcontroller
- GPRS Module
- Pi Camera
- GPS Module
- Speech Recognition Library

**Usage:**

1. Clone the repository to the Raspberry Pi.
2. Install the required dependencies using the provided instructions.
3. Run the main control script to initiate the Intelligent Wheelchair Control System.
