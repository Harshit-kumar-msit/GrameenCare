document.addEventListener("DOMContentLoaded", function () {
    const languageToggle = document.getElementById("language-toggle");

    // Text content in English and Hindi
    const textContent = {
        en: {
            siteTitle: "GrameenCare",
            home: "Home",
            chatbot: "Chatbot",
            tips: "Health Tips",
            contact: "Contact",
            welcomeHeading: "Welcome to GrameenCare",
            welcomeText: "Providing healthcare support for rural communities with AI-powered assistance.",
            chatBtn: "Start Chat",
            toggleText: "हिंदी"
        },
        hi: {
            siteTitle: "ग्रामीनकेयर",
            home: "होम",
            chatbot: "चैटबॉट",
            tips: "स्वास्थ्य सुझाव",
            contact: "संपर्क करें",
            welcomeHeading: "ग्रामीनकेयर में आपका स्वागत है",
            welcomeText: "ग्रामीण समुदायों के लिए एआई-संचालित चिकित्सा सहायता प्रदान करना।",
            chatBtn: "चैट शुरू करें",
            toggleText: "English"
        }
    };

    // Function to switch language
    function switchLanguage(lang) {
        document.getElementById("site-title").textContent = textContent[lang].siteTitle;
        document.getElementById("nav-home").textContent = textContent[lang].home;
        document.getElementById("nav-chatbot").textContent = textContent[lang].chatbot;
        document.getElementById("nav-tips").textContent = textContent[lang].tips;
        document.getElementById("nav-contact").textContent = textContent[lang].contact;
        document.getElementById("welcome-heading").textContent = textContent[lang].welcomeHeading;
        document.getElementById("welcome-text").textContent = textContent[lang].welcomeText;
        document.getElementById("chat-btn").textContent = textContent[lang].chatBtn;
        languageToggle.textContent = textContent[lang].toggleText;

        // Save preference in localStorage
        localStorage.setItem("language", lang);
    }

    // Load saved language preference
    let currentLanguage = localStorage.getItem("language") || "en";
    switchLanguage(currentLanguage);

    // Toggle language on button click
    languageToggle.addEventListener("click", function () {
        currentLanguage = currentLanguage === "en" ? "hi" : "en";
        switchLanguage(currentLanguage);
    });
});
