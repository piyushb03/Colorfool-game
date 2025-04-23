from tkinter import *
import random
from tkinter import messagebox
from tkinter import ttk
import pygame
import os

colours = ['Red','Blue','Green','Gray','Black','Yellow','Orange','White','Purple','Brown']
score = 0
time = 30
game_started = False
best_score = 0

# Initialize pygame mixer
pygame.mixer.init()

# Load best score from file
def load_best_score():
    global best_score
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as file:
            best_score = int(file.read().strip())
    else:
        best_score = 0

# Save best score to file
def save_best_score():
    global best_score
    with open("score.txt", "w") as file:
        file.write(str(best_score))

def play_music():
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def set_time_limit(event=None):
    global time
    time = int(time_combo.get())
    timeLabel.config(text=f"Time left: {time}")

def startGame(event=None):
    global game_started, score
    if not game_started:
        set_time_limit()
        score = 0
        scoreLabel.config(text="Score: 0")
        colour_entry.delete(0, END)
        play_music()
        countdown()
        game_started = True
    nextcolor()

def nextcolor():
    global score, time

    if time > 0:
        colour_entry.focus_set()

        if colour_entry.get().lower() == colours[1].lower():
            score += 1

        colour_entry.delete(0, END)

        random.shuffle(colours)
        colour.config(fg=str(colours[1]), text=str(colours[0]))

        scoreLabel.config(text="Score: " + str(score))

def countdown():
    global time, best_score, game_started

    if time > 0:
        time -= 1
        timeLabel.config(text="Time left: " + str(time))
        timeLabel.after(1000, countdown)
    else:
        stop_music()
        game_started = False
        if score > best_score:
            best_score = score
            save_best_score()
        response = messagebox.askquestion("Game Over", f"Your Score: {score}\nBest Score: {best_score}\n\nPlay Again?")
        if response == "yes":
            startGame()
        else:
            root.destroy()

if __name__ == '__main__':
    load_best_score()

    root = Tk()
    root.title('ColorFool Game by Piyush Baghel')
    root.configure(bg='lightblue')
    root.geometry('600x400')
    root.resizable(0, 0)

    title = Label(root, text='🎨 COLORFOOL GAME 🎮', font=('Algerian', 20, 'bold'), bg='lightblue', fg='darkblue')
    title.pack(pady=15)

    instructions = Label(root, text='Type the COLOR of the word, not the word itself!',
                        font=('Helvetica', 12, 'bold'), bg='lightblue', fg='navy')
    instructions.pack()

    timeFrame = Frame(root, bg='lightblue')
    timeFrame.pack(pady=10)
    timeLabelDrop = Label(timeFrame, text='Select Time Limit:', font=('Arial', 11, 'bold'), bg='lightblue', fg='black')
    timeLabelDrop.pack(side=LEFT, padx=5)

    time_combo = ttk.Combobox(timeFrame, values=[30, 45, 60], width=5, font=('Arial', 10))
    time_combo.current(0)
    time_combo.pack(side=LEFT)
    time_combo.bind("<<ComboboxSelected>>", set_time_limit)

    scoreLabel = Label(root, text='Score: 0', font=('System', 13, 'bold'), bg='lightblue', fg='black')
    scoreLabel.pack(pady=5)

    timeLabel = Label(root, text='Time left: 30', font=('System', 13, 'bold'), bg='lightblue', fg='black')
    timeLabel.pack(pady=5)

    colour = Label(root, font=('Roboto', 30, 'bold'), bg='lightblue')
    colour.pack(pady=25)

    colour_entry = Entry(root, font=('Arial', 16), fg='maroon')
    colour_entry.insert(0, 'Press Enter to Start...')
    colour_entry.bind("<FocusIn>", lambda e: colour_entry.delete(0, END))
    colour_entry.pack(pady=10, ipadx=50, ipady=5)

    root.bind('<Return>', startGame)

    root.mainloop()
