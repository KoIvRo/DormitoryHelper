# Frontend for DormitoryHelper

## For start

In frontend directory
```
npm install
npm start
```

## Description

Frontend application for DormitoryHelper system - announcement board for dormitory. Implemented as SPA (Single Page Application) on React with modern minimalistic design.

## Main features

* User registration and authentication
* View all announcements in real time
* Filter announcements by categories (transport, sale, hobby)
* Create new announcements
* Delete own announcements
* User profile
* Automatic announcement update every 3 seconds (polling)

## Technology stack

* React 18
* React Router DOM for navigation
* Axios for HTTP requests
* CSS for styles (minimalistic design)
* Responsive design

## Project structure

```
announcement-app/
├── src/
│   ├── components/
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── AnnouncementList.js
│   │   ├── AnnouncementForm.js
│   │   ├── UserProfile.js
│   │   └── Navbar.js
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## API connection

The application connects to the backend at `http://localhost:8000`. 
All API requests automatically include JWT token from `localStorage`.

## Available routes

* `/` - Main page with all announcements
* `/login` - User login
* `/register` - User registration
* `/create` - Create new announcement
* `/profile` - User profile with personal announcements

## Requirements

* Node.js 16 or higher
* Backend must be running on http://localhost:8000
* Backend must have CORS configured for http://localhost:3000

## Build for production

```
npm run build
```

## Notes

* The application uses polling to update announcements every 3 seconds
* Users can only delete their own announcements
* JWT token is stored in localStorage
* All forms have validation

## Tools

* React
* React Router
* Axios
* CSS

### Made by

* Korotaev Ivan