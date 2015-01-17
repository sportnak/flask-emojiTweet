# flask-emojiTweet
An application that tweets emojis

Once you've downloaded the code, simply navigate to your application folder and run
'''
flask\Scripts\python run.py
'''

if you want to run the application without debugging simply run '''runp.py''' instead.

## Database Structure

### User

| Name | Type | Data Comments |
| :--------- | :--------- | :--------- |
| Id 		| Int			| Primary Key 	 |
| Nickname	| String(64)	| Index & Unique |
| Email		| String(120)	| Index & Unique |
| Password	| String(54)	| Hashed		 |
| Tweets 	| Relationship	| ref-'Author'	 |
| About_Me	| String(140)	| none			 |
| Last_Seen	| DateTime		| none			 |
| followed	| Relationship	| joins-follows	 |

### Tweets

| Name | Type | Data Comments |
| :--------- | :--------- | :--------- |
| Id 		 | Int 		| Primary Key		 |
| Emoji  	 | Int 		| Foreign Key(Emojis)|
| Timestamp	 | DateTime	| none				 |
| User_Id	 | Int 		| Foreign Key(User)  |

### Emojis

| Name | Type | Data Comments |
| :--------- | :--------- | :--------- |
| Id 		| Int 		 | Primary Key	|
| Location	| String(100)| none			|
| Counter	| Int 		 | none 		|