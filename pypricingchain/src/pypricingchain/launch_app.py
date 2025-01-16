import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

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
        
        colSim, colRf = st.columns(2)

        with colSim:
            n_sim = st.number_input("Enter the number of simulations for the pricing", value=15000, min_value=10000, step=5000)

        with colRf:
             disc_rate = st.number_input("Discount rate for the pricing", value=0.04, min_value=0.0, step=0.01)

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
            st.caption("IMPORTANT: You still have to input dividend yields and risk free rates")

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
            decrement = st.number_input("Decrement value", value=50.0, min_value=0.0)
            st.caption("Please adjust depending on type.")
            st.caption("50 bps per year = 50")
            st.caption("5% per year = 0.05")

        with colPoint:
            decrement_point = st.toggle("Point decrement")

        with colPerc:
            decrement_percentage = st.toggle("Percentage decrement")







        # Price
        if st.button("Price"):
            
            st.markdown('----')

            # Retrieve pricing parameters input
            arr_divs = df_underlyings["Div Yield"].astype(float).values
            arr_rf = df_underlyings["Risk Free Rate"].astype(float).values

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
            
            if from_market:
                price, mat_underlying = pricer.price_from_market_data(arr_divs, arr_rf, disc_rate)

            else:
                arr_vol = df_underlyings["Vol"].astype(float).values
                price, mat_underlying = pricer.price_from_inputs(arr_divs, arr_rf, arr_vol, correl, disc_rate)

            
            # Prepare for an illustration of the trajectories
            fig = plt.Figure(figsize=(10, 6))
            gs = GridSpec(1, 2, width_ratios=[4, 1], wspace=0.2)

            ax_spots = fig.add_subplot(gs[0])
            ax_spots.plot(mat_underlying, alpha=0.8, linewidth=0.7)
            ax_spots.set_xlabel("Time")
            ax_spots.set_ylabel("Underlying level")
            ax_spots.set_title("Simulated Brownians")

            ax_hist = fig.add_subplot(gs[1], sharey=ax_spots)
            ax_hist.hist(mat_underlying[-1, :], bins=100, orientation="horizontal", alpha=0.8)
            ax_hist.set_xlabel("Frequency")
            ax_hist.set_ylabel("")

            st.success(f"Price: {np.round(price*100, 2)}%")

            st.text("Simulated brownians used for the pricing")
            st.pyplot(fig)






    # Multi plateform
    else:
        
        colLeft, colRight = st.columns(2)

        # --------------------------------------------------------
        # Structure 1
        # --------------------------------------------------------


        with colLeft:

            st.subheader("Structure 1 details")
            colSim, colRf = st.columns(2)
            with colSim:
                n_sim1 = st.number_input("Enter the number of simulations for the pricing", value=15000, min_value=10000, step=5000)

            with colRf:
                disc_rate1 = st.number_input("Discount rate for the pricing", value=0.04, min_value=0.0, step=0.01)

            # General paramaters
            st.markdown('----')
            st.text("General parameters")

            colMatu, colUndl, colCoupon = st.columns([1/5, 3/5, 1/5])

            with colMatu:
                maturity1 = st.number_input("Maturity", value=10, min_value=1, step=1)

            with colUndl:
                df_underlyings1 = st.data_editor(pd.DataFrame(index=["Component 1", "Component 2"], columns=["Ticker", "Risk Free Rate", "Div Yield", "Vol"]))
                correl1 = st.number_input("Correlation between assets", -1.0, 1.0, 0.7, 0.01)
                from_market1 = st.toggle("Price using market data")
                st.caption("IMPORTANT: You still have to input dividend yields and risk free rates")

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
                decrement1 = st.number_input("Decrement value", value=50.0, min_value=0.0)
                st.caption("Please adjust depending on type.")
                st.caption("50 bps per year = 50")
                st.caption("5% per year = 0.05")

            with colPoint:
                decrement_point1 = st.toggle("Point decrement")

            with colPerc:
                decrement_percentage1 = st.toggle("Percentage decrement")








        # --------------------------------------------------------
        # Structure 2
        # --------------------------------------------------------



        with colRight:

            st.subheader("Structure 2 details")
            colSim, colRf = st.columns(2)
            
            with colSim:
                n_sim2 = st.number_input("Enter the number of simulations for the pricing", value=15000, min_value=10000, step=5000, key="sim2")

            with colRf:
                disc_rate2 = st.number_input("Discount rate for the pricing", value=0.04, min_value=0.0, step=0.01, key="disc2")

            # General paramaters
            st.markdown('----')
            st.text("General parameters")

            colMatu, colUndl, colCoupon = st.columns([1/5, 3/5, 1/5])

            with colMatu:
                maturity2 = st.number_input("Maturity", value=10, min_value=1, step=1, key="Matu2")

            with colUndl:
                df_underlyings2 = st.data_editor(pd.DataFrame(index=["Component 1", "Component 2"], columns=["Ticker", "Risk Free Rate", "Div Yield", "Vol"]), key="Undl2")
                correl2 = st.number_input("Correlation between assets", -1.0, 1.0, 0.7, 0.01, key="correl2")
                from_market2 = st.toggle("Price using market data", key="mkt2")
                st.caption("IMPORTANT: You still have to input dividend yields and risk free rates")

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
                decrement2 = st.number_input("Decrement value", value=50.0, min_value=0.0, key="dec2")
                st.caption("Please adjust depending on type.")
                st.caption("50 bps per year = 50")
                st.caption("5% per year = 0.05")

            with colPoint:
                decrement_point2 = st.toggle("Point decrement mechanism", key="decp2")

            with colPerc:
                decrement_percentage2 = st.toggle("Percentage decrement", key="decperc2")












        st.markdown('----')
        if st.button("Price"):

                # Build products
                st.markdown('----')

                # Retrieve pricing parameters input
                arr_divs1 = df_underlyings1["Div Yield"].astype(float).values
                arr_rf1 = df_underlyings1["Risk Free Rate"].astype(float).values
                arr_divs2 = df_underlyings2["Div Yield"].astype(float).values
                arr_rf2 = df_underlyings2["Risk Free Rate"].astype(float).values

                # Initialise the products
                phoenix1 = Phoenix(
                    underlying = list(df_underlyings1["Ticker"].values),
                    maturity=maturity1,
                    coupon=coupon1,
                    obs_per_year=obs_per_year1,
                    autocall_barrier=autocall_barrier1,
                    coupon_barrier=coupon_barrier1,
                    put_strike=put_strike1,
                    put_barrier=put_barrier1,
                    decrement=decrement1,
                    decrement_point=decrement_point1,
                    decrement_percentage=decrement_percentage1
                )

                phoenix2 = Phoenix(
                    underlying = list(df_underlyings2["Ticker"].values),
                    maturity=maturity2,
                    coupon=coupon2,
                    obs_per_year=obs_per_year2,
                    autocall_barrier=autocall_barrier2,
                    coupon_barrier=coupon_barrier2,
                    put_strike=put_strike2,
                    put_barrier=put_barrier2,
                    decrement=decrement2,
                    decrement_point=decrement_point2,
                    decrement_percentage=decrement_percentage2
                )


                # Instantiate the pricers
                pricer1 = Pricer(n_sim1, phoenix1)
                pricer2 = Pricer(n_sim2, phoenix2)
                
                # Pricing product 1
                if from_market1:
                    price1, mat_underlying1 = pricer1.price_from_market_data(arr_divs1, arr_rf1, disc_rate1)

                else:
                    arr_vol1 = df_underlyings1["Vol"].astype(float).values
                    price1, mat_underlying1 = pricer1.price_from_inputs(arr_divs1, arr_rf1, arr_vol1, correl1, disc_rate1)

                # Pricing product 2
                if from_market2:
                   price2, mat_underlying2 = pricer2.price_from_market_data(arr_divs2, arr_rf2, disc_rate2)

                else:
                    arr_vol2 = df_underlyings2["Vol"].astype(float).values
                    price2, mat_underlying2 = pricer2.price_from_inputs(arr_divs2, arr_rf2, arr_vol2, correl2, disc_rate2)


                colLeft, colRight = st.columns(2)


                # Display the pricing results
                with colLeft:
                    st.success(f"Price: {np.round(price1*100, 2)}%")
                with colRight:
                    st.success(f"Price: {np.round(price2*100, 2)}%")
                
                # Plot the trajectories
                with colLeft:

                    # Prepare for an illustration of the trajectories
                    fig1 = plt.Figure(figsize=(10, 6))
                    gs1 = GridSpec(1, 2, width_ratios=[4, 1], wspace=0.2)

                    ax_spots1 = fig1.add_subplot(gs1[0])
                    ax_spots1.plot(mat_underlying1, alpha=0.8, linewidth=0.7)
                    ax_spots1.set_xlabel("Time")
                    ax_spots1.set_ylabel("Underlying level")
                    ax_spots1.set_title("Simulated Brownians")

                    ax_hist1 = fig1.add_subplot(gs1[1], sharey=ax_spots1)
                    ax_hist1.hist(mat_underlying1[-1, :], bins=100, orientation="horizontal", alpha=0.8)
                    ax_hist1.set_xlabel("Frequency")
                    ax_hist1.set_ylabel("")


                    st.text("Simulated brownians used for the pricing")
                    st.pyplot(fig1)

                with colRight:

                    # Prepare for an illustration of the trajectories
                    fig2 = plt.Figure(figsize=(10, 6))
                    gs2 = GridSpec(1, 2, width_ratios=[4, 1], wspace=0.2)

                    ax_spots2 = fig2.add_subplot(gs2[0])
                    ax_spots2.plot(mat_underlying2, alpha=0.8, linewidth=0.7)
                    ax_spots2.set_xlabel("Time")
                    ax_spots2.set_ylabel("Underlying level")
                    ax_spots2.set_title("Simulated Brownians")

                    ax_hist2 = fig2.add_subplot(gs2[1], sharey=ax_spots2)
                    ax_hist2.hist(mat_underlying2[-1, :], bins=100, orientation="horizontal", alpha=0.8)
                    ax_hist2.set_xlabel("Frequency")
                    ax_hist2.set_ylabel("")

                    st.text("Simulated brownians used for the pricing")
                    st.pyplot(fig2)