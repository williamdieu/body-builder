# body-builder

## About

Body-builder is a tool designed to scrape bodybuilding.com to create an exercise list which can then be used to generate exercise sessions. This allows for a diverse range of exercises that the user can apply suitable for both beginners (who want to expose themselves to a wide variety) and regulars (who are plateauing due to repetitive motions and wish to fix that).

## Example Usage

As a new user, I need to generate an exercise list so I call `new` which scrapes 75 exercises by default.
I call `display` to see what exercises are in the list. I know I'm not a fan of Atlas Stones so I remove the exercise with `remove` and input `Atlas Stones` when it prompts me.
I wish to target my legs so I call `generate` and input `Quadriceps Hamstrings Calves` with an exercise size of `5`
I am returned a list and try the exercises to see whether I enjoy them and if they are appropriate for me. If not, I call remove so that it can't be picked when I generate another session.



## Potential changes

- Change this to a stand alone program rather than relying on a singular website
