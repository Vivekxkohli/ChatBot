import re
import tkinter as tk
import sqlite3

rule = {
    'Hey|HY|Hello': 'Hey! How may I assist you?',
    'How are you?': 'I am doing great. How may I help you?',
    'What is SLIET|Tell me something about SLIET': 'Sant Longowal Institute of Engineering and Technology (SLIET) is a deemed university located in Longowal, Punjab, India.',
    'What courses are offered by SLIET?|Courses in SLIET': 'SLIET offers undergraduate, postgraduate and doctoral programs in various fields of engineering, technology and sciences.',
    'What is the fee structure at SLIET|Fee structure of SLIET': 'The fee structure varies for different programs like for ICD, its 8900 per semester. You can check the detailed fee structure on the official website of SLIET is sliet.ac.in.',
    'What is the admission process at SLIET': 'Admissions at SLIET are based on entrance exams such as JEE Main, SLIET Entrance Test (SET) and GATE. The university also offers direct admission to some programs based on merit.',
    'What is the contact information for SLIET': 'You can contact SLIET at: \nAddress: Sant Longowal Institute of Engineering and Technology, Longowal - 148106, Distt. Sangrur (Pb.), India \nPhone: +91-1672-253136 \nEmail: sliet@sliet.ac.in',
    ' How many student are studying in SLIET': 'Around 4000 students are studying in SLIET college.',
    'What is the highest package in SLIET?': 'The highest and median package offered was INR 18 LPA and INR 4.10 LPA during SLIET placements 2022, respectively.',
    'Okay|Okay thanks': 'Any other query?',
    'No': 'Okay you can exit the program by typing bye. :)',
    'Where can i find the bookstore on campus': 'At Central Library',
    'List of sports facilities available in campus': 'Sports facilities available in SLIET Campus are:-\nBasket Ball Court\t\tBadminton Court\t\tIndoor Games Room\nFootball Ground\t\tSwimming Pool\t\tGym\nTaekwondo\t\tGatka\t\tSquash\nCricket\t\tVolleyball Court\t\tTable Tennis',
    'What clubs and organizations are available in SLIET': '\nTECHNICAL CLUB :\t\t\t\t\tSOCIAL :\nSSD\t\t\t\t\tN.S.S\nSRAS\t\t\t\t\tSELC\nEndeavour Society\t\t\t\t\tHappy Club\nScience Club\t\t\t\t\tPERSONA SLIET\nIEEE\t\t\t\t\tSLIET Strategic Society\nDiploma Chapter(IE INIDA)\t\t\t\t\tInterWell CLub\nISTE Student Chapter\t\t\t\t\tSviesa - The PhotoGraphy and Movie Club\nSAE India SLIET\t\t\t\t\tHSSC\nMavericks Club\t\t\t\t\tUHV Cell\nIIChE\nHackTekers\nStay Safe Online\n\nSPORTS :\t\t\t\t\tLITERARY :\nSports Committee\t\t\t\t\tFood Technocrats\nPaddler Club\t\t\t\t\tRaj Bhasha Samiti\nSkating Club- Skyliners\t\t\t\t\tANSHUMAT\nNCC\t\t\t\t\tSRIJAN\nHealth Yoga Club\t\t\t\t\tCSSC\nBharat Scouts\t\t\t\t\tCSPDC\n\nCULTURAL :\t\t\t\t\tCOUNSELLING :\nCultural Committee\t\t\t\t\tManodarpan\nSPICMACAY Committee\t\t\t\t\tStudent Mentor & TG\nArt and Decoration Society\t\t\t\t\tScheme\n\t\t\t\t\tClass Counsellor\n\t\t\t\t\tPsychologist Counsellor',
    'How can I contact the SLIET help desk for technical support?': 'Contact : 01672-253602\n                        Email : dracad@sliet.ac.in OR aracad@sliet.ac.in',
    'Are there any upcoming events or workshops on campus?': "You'll get information about upcoming events or workshops on your Department Notice Board OR on your Hostel Notice Board",
    'Can you provide information about hostels?': 'SLIET has established separate hostels for boys and girls\n\n\tBOYS HOSTELS :\nSLIET has 09 Boys Hostels The capacity of each hostels are 235 students, and the capacity of PG Hostel is 80 students\n\nAllocation of Hostel :\nFive three seater Boys Hostels allotted to Certificate and Diploma students\nOne three seater Boys Hostel allotted to First year Degree\nTwo single seater Boys Hostel allotted to Prefinal and final year Degree students\nOne Hostel allotted to PG (MTech. Students)\n\n\tGIRLS HOSTELS :\nSLIET has four Girls Hostel with the capacity of 230 students in each hostel and capacity of PG Girls Hostel is 81  students',
    'What are the campus library hours?': '\n\tGeneral Timings :\n\t\tMonday – Friday	8:30 AM – 7:00 PM\n\t\tSaturday and Sunday	8:30 AM – 5:00 PM\n\t\tHolidays	Closed\n\t\tReading Hall remains open till 12:00 AM\n\n\tCirculation Timings :\n\t\tMonday – Friday	8:30 AM – 6:00 PM\n\t\tSaturday	9:00 AM – 1:00 PM',
    'Where can I find the campus health center?': 'Near Complex In front of KV school',
    'Where can I find the campus Student activity center?': 'In front of Complex',
    'What are the opening hours of the campus gym?':  '\n\tFOR BOYS :\n\t\tMonday – Saturday	4:30 PM – 7:00 PM\n\t\tSunday Closed\n\tFOR GIRLS\n\t\tMonday – Saturday	6:30 AM – 8:30 AM\n\t\tSunday Closed',
    'What is the contact information for the campus health center?': '\n\tTiming : \n\t\t 8:00am to 2:00pm & 2:00pm to 8:00pm \n\t\t(Emergency services: Round the clock on call)',
    'How do I access the campus Wi-Fi network?': 'Connect your Wi-Fi to SLIET Network Then login page appears fill \n"USERNAME" & "PASSWORD" AND PRESS "SIGN IN" ',
    'How do I report a maintenance issue in the hostels?': 'Contact to your hostel BHS, CARETAKER OR to your hostel WARDEN',
    'What are the requirements for graduation?': 'To apply for B.Tech, a candidate must have passed 10+2 in the Science stream. To be selected, they have to take the JEE Main, followed by JoSAA counselling. The JEE Main cut off for the first round is 12,894- 45,074.'
}

# Connect to the database
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()


# Create a table to store the chat history if it doesn't already exist
c.execute(
    '''CREATE TABLE IF NOT EXISTS chat_history(user_input TEXT, message TEXT)''')


def chatbot():
    chat_history_frame = tk.Frame(window)
    chat_history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    chat_history_scrollbar = tk.Scrollbar(chat_history_frame)
    chat_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_history = tk.Text(chat_history_frame, padx=5, pady=5, height=10, width=80, bg="black",
                           fg="yellow", font=("arial", 10), yscrollcommand=chat_history_scrollbar.set)
    chat_history.pack(pady=10, fill=tk.BOTH, expand=True)
    chat_history.tag_configure("right", justify="right")

    chat_history_scrollbar.config(command=chat_history.yview)

    # Add the first message to the chat history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(
        tk.END, "SLIET ChatBot: Welcome! I am your SLIET ChatBot. How can i help you?\n\n", "left")
    chat_history.config(state=tk.DISABLED)

    user_input = tk.Entry(window, bg='white', width=100, font=("arial", 10))
    user_input.pack(pady=10)

    # Set a placeholder for the text box
    user_input.insert(0, "Send a message.")

    def on_entry_click(event):
        if user_input.get() == "Send a message.":
            user_input.delete(0, tk.END)
            user_input.config(bg='white', fg='black')

    def on_focusout(event):
        if user_input.get() == "":
            user_input.insert(0, "Send a message.")
            user_input.config(fg='grey')

    user_input.bind('<FocusIn>', on_entry_click)
    user_input.bind('<FocusOut>', on_focusout)

    def send_message(event=None):
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "\n", "right")
        chat_history.config(state=tk.DISABLED)
        message = user_input.get()
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + message + "\n\n", "right")
        user_input.delete(0, tk.END)

        if message.lower() == "bye":
            chat_history.insert(tk.END, "SLIET ChatBot: TATA!\n")
            conn.commit()  # Commit changes to the database
            conn.close()  # Close the database connection

            return

        match = False
        for key, value in rule.items():
            if re.search(key, message, re.IGNORECASE):
                chat_history.insert(
                    tk.END, "SLIET ChatBot: " + value + "\n\n", "left")
                match = True
                break

        if match == False:
            chat_history.insert(
                tk.END, "SLIET ChatBot: Sorry I couldn't understand your query. Kindly rephrase it.\n Ask Questions like : \n (1) What is SLIET?\n (2) What courses are offered by SLIET?\n (3) What is the fee structure at SLIET?\n                           And many more...\n ", "left")

            # Insert invalid entries into the database
            c.execute("INSERT INTO chat_history VALUES (?, ?)", (message,
                      "Sorry I couldn't understand your query Kindly rephrase it."))
            conn.commit()  # Commit changes to the database

        # Auto-scroll to the bottom of the chat history
        chat_history.yview(tk.END)

    user_input.bind('<Return>', send_message)
    send_button = tk.Button(window, text="Send", font=(
        "Courier New Bold", 14), bg="Blue", fg="White", command=send_message)
    send_button.pack(pady=10)
    window.mainloop()


window = tk.Tk()
window.geometry("610x610")
window.title('SLIET ChatBot')
chatbot()
