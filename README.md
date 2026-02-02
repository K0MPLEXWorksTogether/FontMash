# FontMash
Did you watch *The Social Network*? Remember the website Mark Zuckerberg built? This is something similar. You can cast your vote for your favorite programming font, or watch the leaderboard change as people cast their vote.

## Tech
- This project is built using only two deps - `redis` and `websockets`. The idea is pretty simple.
- Basically, when you load the webpage you make WS connection to my socket. The socket sends a list head-to-head between two fonts, and when you make a choice, the ELO of the winner and loser is updated. 
- A leaderboard of the fonts is sent to all the clients connected for now (I know it's bad, I am planning to only broadcast the changes, later on).
- All font data is stored in a redis sorted set.