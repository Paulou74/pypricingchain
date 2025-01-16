import streamlit as st
import pandas as pd

from pypricingchain.pricer import Pricer
from pypricingchain.phoenix import Phoenix

def launch_app():

    st.set_page_config(
        page_title="pypricingchain",
        layout="wide"
    )

    # General configuration of the page
    if "layout" not in st.session_state:
        st.session_state.layout="centered"


    # Main title
    st.title("Welcome to Pypricingchain")

    # Decide whether to run comparative pricings or single pricing
    multi = st.toggle("Run Comparative pricing")

    # Configuration for the mono pricing
    if not multi:

        st.session_state.layout = "centered"

        st.subheader("Structure details")
        n_sim = st.number_input("Enter the number of simulations for the pricing", value=15000, min_value=10000, step=5000)

        # General paramaters
        st.markdown('----')
        st.text("General parameters")

        colMatu, colUndl, colCoupon = st.columns(3)

        with colMatu:
            maturity = st.number_input("Maturity", value=10, min_value=1, step=1)

        with colUndl:
            df_underlyings = st.data_editor(pd.DataFrame(index=["Component 1", "Component 2"], columns=["Ticker", "Risk Free Rate", "Div Yield", "Vol"]))
            correl = st.number_input("Correlation between assets", -1.0, 1.0, 0.7, 0.01)
            from_market = st.toggle("Price using market data")
            st.caption("IMPORTANT: You still have to input dividend yields")

        with colCoupon:
            coupon = st.number_input("Coupon per period", value=0.05, min_value=0.0, step=0.01)
            st.caption("Example: 5% per period = 0.05. 12% per year = 0.01 for monthly recall")


        st.markdown('----')
        st.text("Recall Frequencies and Barriers")

        colAutocall, colCouponBarrier, colFreq = st.columns(3)

        with colAutocall:
            autocall_barrier = st.number_input("Autocall barrier", value=1.0, min_value=0.0, step=0.05)
            st.caption("Example: Autocall trigger 100%: 1.0")

            put_strike = st.number_input("Put Strike", value=1.0, min_value=0.0, step=0.05)
            st.caption("Example: Put strike 100%: 1.0")


        with colCouponBarrier:
            coupon_barrier = st.number_input("Coupon barrier", value=0.8, min_value=0.0, step=0.05)
            st.caption("Example: Coupon trigger 80%: 0.8")

            put_barrier = st.number_input("Put Barrier", value=1.0, min_value=0.0, step=0.05)
            st.caption("Example: Put barrier 60%: 0.6")

        with colFreq:
            obs_per_year = st.selectbox("Number of observations per year", options=[1, 2, 4, 12])
            st.caption("Monthly observations = 12, Annual observation = 1")


        st.markdown('----')
        st.text("Decrement features")

        colVal, colPoint, colPerc = st.columns(3)

        with colVal:
            decrement = st.number_input("Decrement value", value=50, min_value=0)
            st.caption("Please adjust depending on type.")
            st.caption("50 bps per year = 50")
            st.caption("5% per year = 5")

        with colPoint:
            decrement_point = st.toggle("Point decrement mechanism")

        with colPerc:
            decrement_percentage = st.toggle("Percentage decrement")

        # Price
        if st.button("Price"):

            # Initialise the product
            phoenix = Phoenix(
                underlying = list(df_underlyings["Ticker"].values),
                maturity=maturity,
                coupon=coupon,
                obs_per_year=obs_per_year,
                autocall_barrier=autocall_barrier,
                coupon_barrier=coupon_barrier,
                put_strike=put_strike,
                put_barrier=put_barrier,
                decrement=decrement,
                decrement_point=decrement_point,
                decrement_percentage=decrement_percentage
            )

            # Instantiate the pricer
            pricer = Pricer(n_sim, phoenix)







    else:
        
        colLeft, colRight = st.columns(2)

        # --------------------------------------------------------
        # Structure 1
        # --------------------------------------------------------


        with colLeft:

            st.subheader("Structure 1 details")
            n_sim1 = st.number_input("Enter the number of simulations for the pricing", value=15000, min_value=10000, step=5000)

            # General paramaters
            st.markdown('----')
            st.text("General parameters")

            colMatu, colUndl, colCoupon = st.columns([1/4, 1/2, 1/4])

            with colMatu:
                maturity1 = st.number_input("Maturity", value=10, min_value=1, step=1)

            with colUndl:
                df_underlyings1 = st.data_editor(pd.DataFrame(index=["Component 1", "Component 2"], columns=["Ticker", "Risk Free Rate", "Div Yield", "Vol"]))
                correl1 = st.number_input("Correlation between assets", -1.0, 1.0, 0.7, 0.01)
                from_market1 = st.toggle("Price using market data")
                st.caption("IMPORTANT: You still have to input dividend yields")

            with colCoupon:
                coupon1 = st.number_input("Coupon per period", value=0.05, min_value=0.0, step=0.01)
                st.caption("Example: 5% per period = 0.05. 12% per year = 0.01 for monthly recall")


            st.markdown('----')
            st.text("Recall Frequencies and Barriers")

            colAutocall, colCouponBarrier, colFreq = st.columns(3)

            with colAutocall:
                autocall_barrier1 = st.number_input("Autocall barrier", value=1.0, min_value=0.0, step=0.05)
                st.caption("Example: Autocall trigger 100%: 1.0")

                put_strike1 = st.number_input("Put Strike", value=1.0, min_value=0.0, step=0.05)
                st.caption("Example: Put strike 100%: 1.0")


            with colCouponBarrier:
                coupon_barrier1 = st.number_input("Coupon barrier", value=0.8, min_value=0.0, step=0.05)
                st.caption("Example: Coupon trigger 80%: 0.8")

                put_barrier1 = st.number_input("Put Barrier", value=1.0, min_value=0.0, step=0.05)
                st.caption("Example: Put barrier 60%: 0.6")

            with colFreq:
                obs_per_year1 = st.selectbox("Number of observations per year", options=[1, 2, 4, 12])
                st.caption("Monthly observations = 12, Annual observation = 1")


            st.markdown('----')
            st.text("Decrement features")

            colVal, colPoint, colPerc = st.columns(3)

            with colVal:
                decrement1 = st.number_input("Decrement value", value=50, min_value=0)
                st.caption("Please adjust depending on type.")
                st.caption("50 bps per year = 50")
                st.caption("5% per year = 5")

            with colPoint:
                decrement_point1 = st.toggle("Point decrement mechanism")

            with colPerc:
                decrement_percentage1 = st.toggle("Percentage decrement")








        # --------------------------------------------------------
        # Structure 2
        # --------------------------------------------------------



        with colRight:

            st.subheader("Structure 2 details")
            n_sim2 = st.number_input("Enter the number of simulations for the pricing", value=15000, min_value=10000, step=5000, key="sim2")

            # General paramaters
            st.markdown('----')
            st.text("General parameters")

            colMatu, colUndl, colCoupon = st.columns([1/4, 1/2, 1/4])

            with colMatu:
                maturity2 = st.number_input("Maturity", value=10, min_value=1, step=1, key="Matu2")

            with colUndl:
                df_underlyings2 = st.data_editor(pd.DataFrame(index=["Component 1", "Component 2"], columns=["Ticker", "Risk Free Rate", "Div Yield", "Vol"]), key="Undl2")
                correl2 = st.number_input("Correlation between assets", -1.0, 1.0, 0.7, 0.01, key="correl2")
                from_market2 = st.toggle("Price using market data", key="mkt2")
                st.caption("IMPORTANT: You still have to input dividend yields")

            with colCoupon:
                coupon2 = st.number_input("Coupon per period", value=0.05, min_value=0.0, step=0.01, key="cpn2")
                st.caption("Example: 5% per period = 0.05. 12% per year = 0.01 for monthly recall")


            st.markdown('----')
            st.text("Recall Frequencies and Barriers")

            colAutocall, colCouponBarrier, colFreq = st.columns(3)

            with colAutocall:
                autocall_barrier2 = st.number_input("Autocall barrier", value=1.0, min_value=0.0, step=0.05, key='ac2')
                st.caption("Example: Autocall trigger 100%: 1.0")

                put_strike2 = st.number_input("Put Strike", value=1.0, min_value=0.0, step=0.05, key="pstrike2")
                st.caption("Example: Put strike 100%: 1.0")


            with colCouponBarrier:
                coupon_barrier2 = st.number_input("Coupon barrier", value=0.8, min_value=0.0, step=0.05, key="cpnb2")
                st.caption("Example: Coupon trigger 80%: 0.8")

                put_barrier2 = st.number_input("Put Barrier", value=1.0, min_value=0.0, step=0.05, key="putb2")
                st.caption("Example: Put barrier 60%: 0.6")

            with colFreq:
                obs_per_year2 = st.selectbox("Number of observations per year", options=[1, 2, 4, 12], key="obsfreq")
                st.caption("Monthly observations = 12, Annual observation = 1")


            st.markdown('----')
            st.text("Decrement features")

            colVal, colPoint, colPerc = st.columns(3)

            with colVal:
                decrement2 = st.number_input("Decrement value", value=50, min_value=0, key="dec2")
                st.caption("Please adjust depending on type.")
                st.caption("50 bps per year = 50")
                st.caption("5% per year = 5")

            with colPoint:
                decrement_point2 = st.toggle("Point decrement mechanism", key="decp2")

            with colPerc:
                decrement_percentage2 = st.toggle("Percentage decrement", key="decperc2")

        st.markdown('----')
        if st.button("Price"):

                st.text("Hello")