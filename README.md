## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jamaal001/lfi-scanner
   cd blind_sqli


  2. **usage**
     ```
     python3 main.py -u <target url> -p <payload list>

  3. **vulnerable url lab test**

     ```
     python3 main.py -u https://lfi-lab.onrender.com/file?file= -p /root/Downloads/lif/simple_payloads.txt
