document.addEventListener("DOMContentLoaded", () => {
    // Chat elements
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");
    const chatMessages = document.getElementById("chat-messages");
    
    // Booking elements
    const bookingDateInput = document.getElementById("booking-date");
    const checkSlotsBtn = document.getElementById("check-slots-btn");
    const slotsContainer = document.getElementById("slots-container");
    const slotsGrid = document.getElementById("slots-grid");
    const bookingFormContainer = document.getElementById("booking-form-container");
    const confirmBookingBtn = document.getElementById("confirm-booking-btn");
    const bookingNameInput = document.getElementById("booking-name");
    const bookingEmailInput = document.getElementById("booking-email");
    const bookingStatus = document.getElementById("booking-status");

    let chatHistory = [];
    let selectedSlot = null;

    // Set minimum date to today for calendar booking
    const today = new Date().toISOString().split("T")[0];
    bookingDateInput.min = today;
    bookingDateInput.value = today;

    // ----------------------------------------------------
    // CHAT ENGINE
    // ----------------------------------------------------
    async function sendMessage(text) {
        if (!text.trim()) return;

        // Append user message
        appendMessage("user", text);
        chatInput.value = "";

        // Show typing indicator
        const typingEl = showTypingIndicator();
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const resp = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: text,
                    history: chatHistory
                })
            });

            const data = await resp.json();
            
            // Remove typing indicator
            typingEl.remove();

            if (resp.ok && data.reply) {
                appendMessage("system", data.reply);
                chatHistory.push({ role: "user", content: text });
                chatHistory.push({ role: "assistant", content: data.reply });
            } else {
                appendMessage("system", "Sorry, I encountered an error while processing that request.");
            }
        } catch (err) {
            typingEl.remove();
            appendMessage("system", "Could not connect to the AI service. Please check if the backend is running.");
            console.error(err);
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${sender}-message`;
        
        // Simple markdown parsing for bolding and lists
        let formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');

        msgDiv.innerHTML = formattedText;
        chatMessages.appendChild(msgDiv);
    }

    function showTypingIndicator() {
        const indDiv = document.createElement("div");
        indDiv.className = "message system-message typing-indicator";
        indDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        chatMessages.appendChild(indDiv);
        return indDiv;
    }

    // Input event listeners
    sendBtn.addEventListener("click", () => sendMessage(chatInput.value));
    chatInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            sendMessage(chatInput.value);
        }
    });

    // Handle suggestion chips
    window.sendSuggestion = (text) => {
        sendMessage(text);
    };

    // ----------------------------------------------------
    // SCHEDULER ENGINE
    // ----------------------------------------------------
    async function checkAvailability() {
        const date = bookingDateInput.value;
        if (!date) return;

        bookingStatus.className = "booking-status hidden";
        bookingStatus.textContent = "";
        selectedSlot = null;
        bookingFormContainer.classList.add("hidden");

        try {
            const resp = await fetch(`/api/availability?date=${date}`);
            const data = await resp.json();

            if (!resp.ok) {
                showBookingError(data.detail || "Error retrieving slots.");
                return;
            }

            if (data.error) {
                showBookingError(data.error);
                slotsContainer.classList.add("hidden");
                return;
            }

            slotsGrid.innerHTML = "";
            const slots = data.available_slots;

            if (slots.length === 0) {
                slotsGrid.innerHTML = "<div style='grid-column: span 3; font-size: 13px; color: #ef4444; padding: 10px 0;'>No available slots on this day.</div>";
            } else {
                slots.forEach(slot => {
                    const pill = document.createElement("div");
                    pill.className = "slot-pill";
                    
                    // Format slot text for UI: "09:00" -> "9:00 AM"
                    const [hour, min] = slot.split(":");
                    const hrInt = parseInt(hour);
                    const ampm = hrInt >= 12 ? "PM" : "AM";
                    const displayHr = hrInt > 12 ? hrInt - 12 : hrInt === 0 ? 12 : hrInt;
                    pill.textContent = `${displayHr}:${min} ${ampm}`;
                    
                    pill.dataset.value = slot;

                    pill.addEventListener("click", () => {
                        // De-select previous
                        const currentSelected = slotsGrid.querySelector(".slot-pill.selected");
                        if (currentSelected) currentSelected.classList.remove("selected");

                        pill.classList.add("selected");
                        selectedSlot = slot;
                        
                        // Reveal booking details form
                        bookingFormContainer.classList.remove("hidden");
                    });

                    slotsGrid.appendChild(pill);
                });
            }

            slotsContainer.classList.remove("hidden");
        } catch (err) {
            showBookingError("Failed to fetch slots. Backend is offline.");
            console.error(err);
        }
    }

    async function confirmBooking() {
        const date = bookingDateInput.value;
        const name = bookingNameInput.value;
        const email = bookingEmailInput.value;

        if (!selectedSlot) {
            showBookingError("Please pick a time slot first.");
            return;
        }

        if (!name.trim() || !email.trim()) {
            showBookingError("Name and Email are required.");
            return;
        }

        bookingStatus.className = "booking-status hidden";

        try {
            const resp = await fetch("/api/book", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    date: date,
                    time: selectedSlot
                })
            });

            const data = await resp.json();

            if (resp.ok) {
                // Success!
                bookingStatus.className = "booking-status success";
                bookingStatus.textContent = data.message;
                
                // Clear state
                bookingNameInput.value = "";
                bookingEmailInput.value = "";
                selectedSlot = null;
                bookingFormContainer.classList.add("hidden");
                
                // Trigger assistant reply to confirm booking context in chat
                appendMessage("system", `🤖 **Appointment Confirmed!** I have scheduled your interview with Yash for **${date}** at **${data.booking.time}**. A calendar invitation has been sent to **${email}**.`);
                
                // Refresh slots
                checkAvailability();
            } else {
                showBookingError(data.detail || "Booking failed.");
            }
        } catch (err) {
            showBookingError("Network error. Could not book interview.");
            console.error(err);
        }
    }

    function showBookingError(msg) {
        bookingStatus.className = "booking-status error";
        bookingStatus.textContent = msg;
        bookingStatus.classList.remove("hidden");
    }

    // Booking Event Listeners
    checkSlotsBtn.addEventListener("click", checkAvailability);
    confirmBookingBtn.addEventListener("click", confirmBooking);
});
