This project presents a secure cloud storage solution that integrates authentication-based access control and file storage using Mega Drive. 
Traditional cloud storage platforms often lack advanced authentication mechanisms, leaving user data vulnerable to unauthorized access. 
To address this, the system implements a secure authentication process before allowing file uploads, ensuring only authorized users can store and retrieve data.
The project is built using Flask for backend operations, Firebase for authentication, and the Mega API for cloud storage management. 
The authentication process supports email-password verification, multi-factor authentication, and session management to enhance security. 
Once authenticated, users can seamlessly upload files, which are automatically stored in Mega Drive.
The system offers encryption features to ensure data security during transmission and storage. 
Additionally, user activity logs provide forensic tracking capabilities. 
Future enhancements may include real-time file monitoring, access control policies, and integration with other cloud platforms to improve scalability and reliability.
