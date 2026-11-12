import streamlit as st

st.set_page_config(layout="wide")

icon_col, title_col = st.columns([1, 10], vertical_alignment="center")

with icon_col:
    st.image("assets/egg_chef.jpg", width=200)

with title_col:
    st.title("Recipe & Grocery Assistant")

# embedded css and svg paper filters
st.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Oregano:ital@0;1&display=swap');

        /* paper texture using single-line svg data uri */
        :root {
            --paper-wrinkle-texture: url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 250 250' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.04' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='matrix' values='1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.07 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        }

        /* lined notebook paper */
        .notebook-page {
            position: relative;
            background-color: ##f5f3f0;
            background-image: 
                var(--paper-wrinkle-texture),
                /* crease shading */
                linear-gradient(
                    135deg, rgba(255,255,255,0.4) 0%, 
                    rgba(0,0,0,0.02) 40%, 
                    rgba(0,0,0,0.06) 50%, 
                    rgba(255,255,255,0.2) 60%
                ),
                /* vertical red margin */
                linear-gradient(90deg, transparent 48px, #f28b9f 48px, #f28b9f 50px, transparent 50px),
                /* horizontal blue ruled lines */
                linear-gradient(#bcd2e8 1px, transparent 1px);
            background-size: auto, 100% 100%, 100% 100%, 100% 30px;
            line-height: 30px;
            padding: 32px 24px 30px 62px;
            border-radius: 2px 8px 8px 3px;
            box-shadow:
                0 1px 3px rgba(0,0,0,0.12),
                4px 8px 18px rgba(0,0,0,0.14),
                inset 0 0 60px rgba(220, 205, 175, 0.35);
            border: 1px solid #e2dac9;
            font-family: 'Oregano', cursive;
            font-size: 1.15rem;
            color: #2b2b2b;
            min-height: 480px;
        }

        /* ripped paper */
        .ripped-paper {
            position: relative;
            background-color: ##f5f3f0;
            background-image: 
                var(--paper-wrinkle-texture),
                /* diagonal wrinkle shadows and crumple highlights */
                linear-gradient(115deg, rgba(255,255,255,0.7) 0%, rgba(0,0,0,0.03) 25%, rgba(255,255,255,0.4) 50%, rgba(0,0,0,0.04) 75%),
                /* vertical pink/red legal pad margin */
                linear-gradient(90deg, transparent 38px, rgba(240, 130, 130, 0.45) 38px, rgba(240, 130, 130, 0.45) 39px, transparent 39px),
                /* faint horizontal writing lines across the entire sheet */
                linear-gradient(rgba(215, 205, 175, 0.4) 1px, transparent 1px);
            background-size: auto, 100% 100%, 100% 100%, 100% 28px;
            line-height: 28px;
            padding: 34px 22px 34px 48px;
            font-family: 'Oregano', cursive;
            font-size: 1.15rem;
            color: #2e2e2e;
            min-height: 480px;
            /* organic, varied tears across top and bottom */
            clip-path: polygon(
                0% 16px, 3% 4px, 7% 17px, 11% 3px, 15% 15px, 19% 5px, 24% 18px, 28% 2px, 
                33% 14px, 38% 6px, 42% 16px, 47% 3px, 52% 17px, 57% 5px, 62% 15px, 67% 2px, 
                72% 16px, 77% 4px, 82% 18px, 87% 3px, 92% 15px, 96% 5px, 100% 14px,
                100% calc(100% - 15px), 96% calc(100% - 3px), 91% calc(100% - 14px), 86% calc(100% - 4px),
                81% calc(100% - 16px), 76% calc(100% - 2px), 70% calc(100% - 15px), 64% calc(100% - 5px),
                58% calc(100% - 17px), 52% calc(100% - 3px), 46% calc(100% - 14px), 40% calc(100% - 6px),
                34% calc(100% - 16px), 28% calc(100% - 2px), 22% calc(100% - 15px), 16% calc(100% - 4px),
                10% calc(100% - 17px), 5% calc(100% - 3px), 0% calc(100% - 13px)
            );
            filter: drop-shadow(2px 6px 14px rgba(0, 0, 0, 0.15));
        }

        /* notebook binder punch holes along the left margin */
        .notebook-page::before {
            content: '';
            position: absolute;
            left: 14px;
            top: 24px;
            bottom: 20px;
            width: 14px;
            background-image: radial-gradient(circle 6px at 7px 7px, #fafafa 90%, transparent 95%);
            background-size: 14px 70px;
        }

        .paper-title {
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: 14px;
            background-image: linear-gradient(to right, #6e6e6e 50%, transparent 50%);
            background-position: bottom;
            background-size: 15px 1.5px;
            background-repeat: repeat-x;
            padding-bottom: 6px;
            padding-bottom: 6px;
            letter-spacing: 0.5px;
        }
    </style>
""")

spacer_col, recipe_col, spacer_col, groceries_col, spacer_col = st.columns([0.5, 2, 1, 2, 0.5])

# recipe on notebook paper
with recipe_col:
    st.markdown("""
    <div class="notebook-page">
        <div class="paper-title">Personalized Recipe</div>
        <p>Your personalized recipe will appear here.</p>
    </div>
    """, unsafe_allow_html=True)

# groceries on ripped page
with groceries_col:
    st.markdown("""
    <div class="ripped-paper">
        <div class="paper-title">Grocery List</div>
        <p>Your grocery list will appear here.</p>
    </div>
    """, unsafe_allow_html=True)

user_prompt = st.chat_input("Ask for a recipe or paste a URL...", max_chars=1000)

if user_prompt:
    # update this calculation. currently ~1 token per 4 characters
    estimated_tokens = round(len(user_prompt) / 4)
    st.caption(f"Input received: {len(user_prompt)} characters (~{estimated_tokens} tokens)")