# sos.py

import streamlit as st

TRIGGER_WORDS = [
    "suicide", "kill myself", "end my life", "i want to die",
    "hurt myself", "self harm", "hopeless", "cut myself",
    "no reason to live", "give up", "depressed", "overdose"
]

def check_for_sos_trigger(user_input: str) -> bool:
    """Checks if the user's input contains any trigger words."""
    user_input = user_input.lower()
    return any(word in user_input for word in TRIGGER_WORDS)

def get_sos_modal_html() -> str:
    """
    Generates a self-contained HTML, CSS, and JavaScript modal.
    The JavaScript handles all closing logic internally without needing
    to communicate back to Streamlit's Python backend.
    """
    return """
    <style>
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.7);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.2s ease-in-out;
        }
        .modal-content {
            background: #1e1f20;
            color: #e8eaed;
            padding: 2rem;
            border-radius: 12px;
            max-width: 500px;
            width: 90%;
            position: relative;
            border: 1px solid #5f6368;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }
        .close-button {
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 1.5rem;
            color: #9aa0a6;
            cursor: pointer;
            border: none;
            background: none;
        }
        .close-button:hover { color: #ffffff; }
        .modal-content h2 { color: #f28b82; margin-top: 0; }
        .modal-content a { color: #8ab4f8; text-decoration: none; }
        
        @keyframes fadeInSlideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>

    <div id="sosModal" class="modal-overlay">
        <div class="modal-content">
            <button class="close-button" id="closeSosBtn">×</button>
            <h2>🚨 Urgent Support Resources</h2>
            <p>If you're in immediate distress or feel unsafe, <strong>please contact a mental health professional or crisis service.</strong></p>
            <h4>📞 Emergency Helplines (India):</h4>
            <ul>
                <li><strong>iCall (TISS):</strong> <a href="tel:+919152987821">+91-9152987821</a></li>
                <li><strong>AASRA:</strong> <a href="tel:+919820466726">+91-9820466726</a></li>
                <li><strong>KIRAN Mental Health:</strong> <a href="tel:18005990019">1800-599-0019</a></li>
            </ul>
            <h4>🏥 Vadodara Facilities:</h4>
            <ul><li>Parul Sevashram Hospital</li><li>SSG Hospital Psychiatry Dept.</li></ul>
            <p>🛑 If it's a medical emergency, please dial <a href="tel:108"><strong>108</strong></a>.</p>
        </div>
    </div>

    <script>
        // This script is now fully self-contained.
        // It finds the modal and attaches event listeners to close it.
        const modal = document.getElementById('sosModal');
        const closeButton = document.getElementById('closeSosBtn');

        const closeModal = () => {
            if (modal) {
                modal.style.display = 'none';
            }
        };

        // Attach listeners only if the elements exist
        if (modal && closeButton) {
            // Close via 'x' button
            closeButton.onclick = closeModal;

            // Close via click outside the content box
            modal.onclick = function(event) {
                if (event.target === modal) {
                    closeModal();
                }
            };
            
            // Close via Escape key
            document.addEventListener('keydown', function(event) {
                if (event.key === "Escape") {
                    closeModal();
                }
            });
        }
    </script>
    """


# # sos.py

# import streamlit as st

# TRIGGER_WORDS = [
#     "suicide", "kill myself", "end my life", "i want to die",
#     "hurt myself", "self harm", "hopeless", "cut myself",
#     "no reason to live", "give up", "depressed", "overdose"
# ]

# def check_for_sos_trigger(user_input: str) -> bool:
#     """Checks if the user's input contains any trigger words."""
#     user_input = user_input.lower()
#     return any(word in user_input for word in TRIGGER_WORDS)

# def get_sos_modal_html() -> str:
#     """
#     Generates a self-contained HTML, CSS, and JavaScript modal.
#     This version uses a more robust JavaScript implementation to ensure
#     the close button works reliably within Streamlit's lifecycle.
#     """
#     return """
#     <style>
#         .modal-overlay {
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100vw;
#             height: 100vh;
#             background: rgba(0, 0, 0, 0.7);
#             z-index: 9999;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#         }
#         .modal-content {
#             background: #1e1f20;
#             color: #e8eaed;
#             padding: 2rem;
#             border-radius: 12px;
#             max-width: 500px;
#             width: 90%;
#             position: relative;
#             border: 1px solid #5f6368;
#             box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
#         }
#         .close-button {
#             position: absolute;
#             top: 10px;
#             right: 15px;
#             font-size: 1.5rem;
#             color: #9aa0a6;
#             cursor: pointer;
#             border: none;
#             background: none;
#         }
#         .close-button:hover { color: #ffffff; }
#         .modal-content h2 { color: #f28b82; margin-top: 0; }
#         .modal-content a { color: #8ab4f8; text-decoration: none; }
#     </style>

#     <div id="sosModal" class="modal-overlay">
#         <div class="modal-content">
#             <button class="close-button" id="closeSosBtn">×</button>
#             <h2>🚨 Urgent Support Resources</h2>
#             <p>If you're in immediate distress or feel unsafe, <strong>please contact a mental health professional or crisis service.</strong></p>
#             <h4>📞 Emergency Helplines (India):</h4>
#             <ul>
#                 <li><strong>iCall (TISS):</strong> <a href="tel:+919152987821">+91-9152987821</a></li>
#                 <li><strong>AASRA:</strong> <a href="tel:+919820466726">+91-9820466726</a></li>
#                 <li><strong>KIRAN Mental Health:</strong> <a href="tel:18005990019">1800-599-0019</a></li>
#             </ul>
#             <h4>🏥 Vadodara Facilities:</h4>
#             <ul><li>Parul Sevashram Hospital</li><li>SSG Hospital Psychiatry Dept.</li></ul>
#             <p>🛑 If it's a medical emergency, please dial <a href="tel:108"><strong>108</strong></a>.</p>
#         </div>
#     </div>

#     <script>
#         // This is a more robust way to ensure the script runs and the listeners are attached.
#         function setupModal() {
#             const modal = document.getElementById('sosModal');
#             const closeButton = document.getElementById('closeSosBtn');

#             if (!modal || !closeButton) {
#                 // If elements aren't found, try again in a moment.
#                 // This handles Streamlit's rendering timing.
#                 setTimeout(setupModal, 100);
#                 return;
#             }

#             const closeModal = () => {
#                 modal.style.display = 'none';
#             };

#             // Close via 'x' button
#             closeButton.addEventListener('click', closeModal);

#             // Close via click outside the content box
#             modal.addEventListener('click', function(event) {
#                 if (event.target === modal) {
#                     closeModal();
#                 }
#             });
            
#             // Close via Escape key
#             document.addEventListener('keydown', function(event) {
#                 if (event.key === "Escape") {
#                     closeModal();
#                 }
#             });
#         }

#         // Start the setup process
#         setupModal();
#     </script>
#     """