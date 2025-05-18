import streamlit as st
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# --- Config
st.set_page_config(
    page_title="24Hourglass",
    page_icon="⏳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Auto-refresh every second (1000 ms)
st_autorefresh(interval=1000, key="abacusclock")

# --- Abacus Layout Spec
UNIT_CONFIGS = {
    "S": {"columns": [("1", 4), ("5", 1), ("10", 2), ("30", 1)], "max": 60},
    "M": {"columns": [("1", 4), ("5", 1), ("10", 2), ("30", 1)], "max": 60},
    "H": {"columns": [("1", 2), ("3", 1), ("6", 1), ("12", 1)], "max": 24},
}

COLORS = {
    "active": "●",  # or ⬤, ●, 🟠
    "inactive": "·"
}

# Common timezones for the selector
COMMON_TIMEZONES = [
    'UTC',
    'US/Pacific',
    'US/Eastern',
    'Europe/London',
    'Europe/Paris',
    'Asia/Tokyo',
    'Asia/Shanghai',
    'Australia/Sydney',
]

def abacus_decompose(value, columns):
    """
    Decompose a value into an abacus representation.
    
    Args:
        value: The time value to represent (hours, minutes, or seconds)
        columns: Column configuration with denominations and bead counts
        
    Returns:
        A grid representation of the abacus beads (1=active, 0=inactive)
    """
    beads_columns = []
    remaining = value
    for label, bead_count in reversed(columns):
        denom = int(label)
        beads_on = min(remaining // denom, bead_count)
        remaining -= beads_on * denom
        beads = [1] * beads_on + [0] * (bead_count - beads_on)
        beads_columns.insert(0, beads)  # Insert leftmost column first
    # Now, to render row-by-row, determine the max height and build each row
    max_rows = max(len(col) for col in beads_columns)
    grid = []
    for row in range(max_rows):
        this_row = []
        for col in beads_columns:
            # pad top with None for columns with fewer beads
            if row < max_rows - len(col):
                this_row.append('')  # blank, not a dot
            else:
                idx = row - (max_rows - len(col))
                bead = col[idx]
                this_row.append(bead)
        grid.append(this_row)
    return grid

def abacus_unit(name, value, config):
    """
    Render an abacus unit (hours, minutes, or seconds) in the Streamlit UI.
    
    Args:
        name: The name of the unit (H, M, S)
        value: The current value
        config: The configuration for this unit
    """
    columns = config["columns"]
    col_labels = [label for label, _ in columns]
    grid = abacus_decompose(value, columns)
    # Header
    st.markdown(
        f"<div style='text-align:center; color:#d4af37; font-weight:bold; font-size:1.1em; margin-bottom:0.1em;'>{name}</div>",
        unsafe_allow_html=True
    )
    # Column headers
    st.markdown(
        "<div style='display:grid;grid-template-columns:repeat(%d,1fr);background:#1a5276;color:white;text-align:center;padding:3px 0;border-bottom:1.5px solid #d4af37;'>%s</div>"
        % (len(col_labels), "".join(f"<div>{c}</div>" for c in col_labels)),
        unsafe_allow_html=True
    )
    # Grid
    st.markdown("<div style='background:#222831;padding:8px 0 8px 0;'>", unsafe_allow_html=True)
    for row in grid:
        st.markdown(
            "<div style='display:grid;grid-template-columns:repeat(%d,1fr);height:28px;text-align:center;'>" % len(row) +
            "".join(
                f"<div style='font-size:1.6em; color: {'#f39c12' if b==1 else '#6c757d'};'>{COLORS['active'] if b==1 else (COLORS['inactive'] if b==0 else '')}</div>"
                for b in row
            ) + "</div>",
            unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def display_digital_time(now, timezone):
    """Display digital time in HH:MM:SS format with timezone info"""
    st.markdown(
        f"<div style='background:#1d2d44;color:#fff;text-align:center;padding:12px 0;margin-bottom:0.5em;border:1.5px solid #d4af37;font-size:1.3em;font-weight:bold;width:100%;'>{now.strftime('%H:%M:%S')} <span style='font-size:0.7em;'>{timezone}</span></div>",
        unsafe_allow_html=True,
    )

def get_current_time(timezone='UTC'):
    """Get current time in the specified timezone"""
    try:
        tz = pytz.timezone(timezone)
        return datetime.now(tz)
    except:
        # Fallback to UTC in case of any issues
        return datetime.now(pytz.UTC)

def timezone_selector():
    """Display timezone selector and return the selected timezone"""
    # Initialize session state for timezone if it doesn't exist
    if 'timezone' not in st.session_state:
        # Try to get the local timezone, fallback to UTC
        try:
            local_tz = datetime.now().astimezone().tzinfo.tzname(None)
            # Map common name to pytz name if possible
            if local_tz in pytz.all_timezones:
                st.session_state.timezone = local_tz
            else:
                st.session_state.timezone = 'UTC'
        except:
            st.session_state.timezone = 'UTC'
    
    # Create a container with custom styling for the timezone selector
    with st.container():
        st.markdown(
            """
            <div style='display:flex; justify-content:flex-end; margin-bottom:10px;'>
                <div style='font-size:0.8em; color:#d4af37; margin-right:5px; line-height:30px;'>Timezone:</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Place the selector in a narrow column
        col1, col2 = st.columns([4, 1])
        with col2:
            selected_tz = st.selectbox(
                label="Timezone",
                options=COMMON_TIMEZONES,
                index=COMMON_TIMEZONES.index(st.session_state.timezone) if st.session_state.timezone in COMMON_TIMEZONES else 0,
                label_visibility="collapsed"
            )
            st.session_state.timezone = selected_tz
            
    return selected_tz

def main():
    """Main application function"""
    # Get timezone selection
    selected_timezone = timezone_selector()
    
    # Get current time in selected timezone
    now = get_current_time(selected_timezone)
    h, m, s = now.hour, now.minute, now.second
    
    # Display digital time
    display_digital_time(now, selected_timezone)
    
    # Display abacus units
    abacus_unit("S", s, UNIT_CONFIGS["S"])
    abacus_unit("M", m, UNIT_CONFIGS["M"])
    abacus_unit("H", h, UNIT_CONFIGS["H"])

if __name__ == "__main__":
    main()
