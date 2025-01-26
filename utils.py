# utils.py

#The reason for this file is to create functions for code 
# that will be repeated with the aim to follow DRY priciples


from datetime import datetime
from flask import flash, redirect, url_for, session, Flask
from models import user_interaction, db


def convertBirthday(birthday_str, flash_category='signup' or 'login'):
    """Converts birthday string to a date object. Returns None if conversion fails."""
    try:
        return datetime.strptime(birthday_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid birthday format. Please use YYYY-MM-DD", flash_category)
        return None

def commitUserInteraction(topic):


        #Commits user interaction data for a specific topic to the database.

        userId = session.get('userId')  # Ensure user ID is stored in session

        if userId:
           interaction = user_interaction.query.filter_by(userId=userId, topic = topic).first()
           if interaction:
              interaction.clickCount += 1 #this will add a count everytime the user interacts with this topic
           else:
            interaction = user_interaction(userId=userId, topic=topic)
            db.session.add(interaction)

            #commit changes
           db.session.commit()


#we don't have a database for our threats topics
#I'm mapping the topics images to use for the 
# profile page for User's Favorite Topics
#this data gets called in profile route and profile.html
topicImage = {
    "Ransomware": "static/img/Ransomware.png",
    "Social Engineering": "static/img/Social_Engineering.png",
    "Cyber Hygiene": "static/img/Cyber_Hygiene.png",
    "IoT": "static/img/IoT.png",
    "Phishing Scams": "static/img/Phishing.png"
}

#I'll also be feeding the start of each Topic 
# description to use in User's Favorite Topics
#this data gets called in profile route and profile.html
topicGraph = {
    "Ransomware": "Ransomware is a type of malicious software designed to block access to a computer system...",
    "Social Engineering": "...attacks manipulate people into sharing information that they shouldn’t share...",
    "Cyber Hygiene": "...essential if you want to keep yourself protected...",
    "IoT": "IoT (Internet of Things) device hacking refers to exploiting vulnerabilities in internet-connected devices...",
    "Phishing Scams": "...a technique used by hackers to trick people into giving personal details or taking an action..."
}

#adding a hardcoded list for topics, this can be imporved on when database is added.
ALL_TOPICS = ['Phishing Scams', 'IoT', 'Social Engineering', 'Ransomware', 'Cyber Hygiene']
totalTopics = len(ALL_TOPICS)

def get_total_topics():  # Had to insert this code because of circular import. If you need to remove it, please do so - T
    return totalTopics
