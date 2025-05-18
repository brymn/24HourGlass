# 24HourGlass

A digital abacus-style clock visualization using Streamlit that represents time in an elegant and unique way.

## Overview

24HourGlass is a web application that displays the current time using an abacus-inspired visualization. Each time unit (hours, minutes, seconds) is represented as a set of beads on weighted columns, creating a visually novel and functional timepiece.

**Note:** This project was "vibe coded" - meaning it was created in a flow state with an emphasis on creative expression rather than being meticulously planned and hand-coded from scratch.

## Features

- Real-time clock display updating every second
- Abacus-style visualization for hours, minutes, and seconds
- Timezone selection for viewing time across different regions
- Elegant gold and dark color scheme

## How It Works

The time display uses the following column structure:
- **Hours**: 1, 3, 6, and 12-hour increments (24-hour format)
- **Minutes**: 1, 5, 10, and 30-minute increments
- **Seconds**: 1, 5, 10, and 30-second increments

Active beads are displayed in orange, while inactive beads are in gray.

## Installation

1. Clone this repository:
```
git clone https://github.com/brymn/24HourGlass.git
cd 24hourglass
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the application with Streamlit:
```
streamlit run abacus_clock.py
```

The application will open in your default web browser. Use the timezone selector in the upper right corner to view the time in different regions.

## Requirements

- Python 3.7+
- Streamlit
- streamlit-autorefresh
- pytz

## Acknowledgments

- Inspired by abacus counting systems and digital time displays
- Built with Streamlit (https://streamlit.io/) 
