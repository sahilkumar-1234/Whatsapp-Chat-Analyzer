
# WhatsApp Chat Analyzer 📊💬

A data analysis tool built using Python and Streamlit to analyze WhatsApp chat exports. It provides insights into your chat data through various visualizations like word clouds, timelines, activity heatmaps, most active users, and more.


![Streamlit Screenshot]<img width="1919" height="900" alt="image" src="https://github.com/user-attachments/assets/ba3298b3-2036-4351-be11-f052d8de346d" />
)

---
## Tool Url Link:[https://whatsapp-chat-analyzer-web.streamlit.app/]
---

## 🚀 Features

- 📅 Daily, monthly, and weekly timeline analysis
- ⏰ Activity heatmap (most active hours/days)
- 🧑‍🤝‍🧑 Most active users (in group chats)
- 🔤 Most common words (WordCloud + bar chart)
- 😂 Emoji analysis (emoji frequency count)
- 📁 Easy chat file upload and parsing

---

## 🛠️ Technologies Used

- **Python** 🐍
- **Pandas** for data manipulation
- **Streamlit** for interactive web UI
- **Matplotlib**, **Seaborn**, **WordCloud**, and **Plotly** for visualizations
- **Regex** for preprocessing chat data

---
# 📂 How to Run Locally

1.**Clone the repository**
   ```bash
   git clone https://github.com/sahilkumar-1234/Whatsapp-Chat-Analyzer.git
   cd Whatsapp-Chat-Analyzer
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

4. **Upload a WhatsApp `.txt` chat export** and start analyzing!

---

## 📸 Sample Output

| WordCloud                                                                                                        | Activity Map                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| ![wordcloud](<img width="1122" height="693" alt="image" src="https://github.com/user-attachments/assets/6f96b1b6-248a-477b-aa19-90519fede6a9" />
) | ![heatmap](<img width="1460" height="676" alt="image" src="https://github.com/user-attachments/assets/34b0bc87-0bbd-4dc9-b539-1ced1b587ba3" />
) |

---

## 📥 Exporting Your WhatsApp Chat

1. Open WhatsApp
2. Go to the chat/group you want to analyze
3. Click on the 3-dot menu → More → Export Chat → *Without Media*
4. Upload the `.txt` file into the analyzer

---

## 📌 To Do

* Add NLP-based sentiment analysis
* Support for media-rich exports
* Add filters for specific users or dates

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Developed with ❤️ by [Sahil Kumar](https://github.com/sahilkumar-1234)
