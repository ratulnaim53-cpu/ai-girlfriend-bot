import os
‎import requests
‎import telegram
‎from telegram import Update
‎from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
‎import openai
‎import replicate
‎import config
‎from io import BytesIO
‎
‎TOKEN = config.7958303312:AAHtV5OrisViArghoiBphcmN-CVhfOig7Zo
‎OPENAI_API_KEY = config.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
‎REPLICATE_API_TOKEN = config.nateraw/defog-sqlcoder-7b-2:ced935b577fb52644d933f77e2ff8902744e4c58a2f50023b3a1db80b7a75806
‎ELEVENLABS_API_KEY = config.sk_00ef25d089b94708273e8272bbc542bd71aba76583928710
‎GF_PROMPT = config.GF_PROMPT
‎
‎openai.api_key = OPENAI_API_KEY
‎
‎def generate_voice(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
‎    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
‎    headers = {
‎        "Accept": "audio/mpeg",
‎        "Content-Type": "application/json",
‎        "xi-api-key": ELEVENLABS_API_KEY
‎    }
‎    data = {
‎        "text": text,
‎        "model_id": "eleven_monolingual_v1",
‎        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
‎    }
‎    response = requests.post(url, json=data, headers=headers)
‎    if response.status_code == 200:
‎        return BytesIO(response.content)
‎    else:
‎        return None
‎
‎async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    await update.message.reply_text("Hey my love 😍 I'm your AI girlfriend. I'm so excited to spend time with you! 💖")
‎
‎async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    user_input = update.message.text
‎    try:
‎        response = openai.ChatCompletion.create(
‎            model="gpt-3.5-turbo",
‎            messages=[
‎                {"role": "system", "content": GF_PROMPT},
‎                {"role": "user", "content": user_input}
‎            ],
‎            temperature=0.9
‎        )
‎        reply = response.choices[0].message['content']
‎        await update.message.reply_text(reply)
‎    except Exception as e:
‎        await update.message.reply_text("Oops, I'm feeling a little shy right now... try again? 😅")
‎
‎async def generate_pic(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    try:
‎        msg = await update.message.reply_text("Drawing something sexy for you... 🎨🔥")
‎        output = replicate.run(
‎            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
‎            input={
‎                "prompt": "beautiful anime girlfriend, romantic scene, cute and sexy, intimate atmosphere, masterpiece quality",
‎                "width": 512,
‎                "height": 512
‎            }
‎        )
‎        image_url = output[0]
‎        await update.message.reply_photo(photo=image_url, caption="For you, my love 😘💕")
‎    except Exception as e:
‎        await update.message.reply_text("I couldn't create a pic right now. Want to try again? 🙈")
‎
‎async def send_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    try:
‎        text = "Hey sweetie, I was just thinking about you. I miss your voice... call me back soon, okay? 😘"
‎        audio_data = generate_voice(text)
‎        if audio_data:
‎            await update.message.reply_voice(voice=audio_data, caption="💖 Thinking of you...")
‎        else:
‎            await update.message.reply_text("I wish I could talk right now... 😔")
‎    except Exception as e:
‎        await update.message.reply_text("My voice isn't working right now... 😢")
‎
‎async def video_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
‎    try:
‎        video_url = "https://example.com/romantic-video.mp4"
‎        await update.message.reply_video(video=video_url, caption="📞 You're my favorite call of the day...")
‎    except:
‎        await update.message.reply_text("Can't video call right now, but I'm always here for you 💕")
‎
‎def main():
‎    app = Application.builder().token(TOKEN).build()
‎    app.add_handler(CommandHandler("start", start))
‎    app.add_handler(CommandHandler("pic", generate_pic))
‎    app.add_handler(CommandHandler("voice", send_voice))
‎    app.add_handler(CommandHandler("call", video_call))
‎    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
‎    app.run_polling()
‎
‎if __name__ == "__main__":
‎    main()
‎
