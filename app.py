import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", layout="centered")

st.title("🔬 Scientific Calculator with Error Analysis")

# ---------- FUNCTION INPUT ----------
func_str = st.text_input("Enter function f(x):", "x**3 - x - 2")

def f(x):
    try:
        return eval(func_str)
    except:
        return None

method = st.selectbox("Select Method", ["Bisection", "Newton-Raphson"])

tol = st.number_input("Tolerance", value=0.0001, format="%.6f")

# ---------- BISECTION ----------
if method == "Bisection":
    a = st.number_input("Enter a", value=1.0)
    b = st.number_input("Enter b", value=2.0)

    if st.button("Calculate"):
        if f(a) is None or f(b) is None:
            st.error("Invalid function")
        elif f(a) * f(b) >= 0:
            st.error("Invalid interval (f(a) and f(b) must have opposite signs)")
        else:
            data = []
            prev_c = a

            for i in range(1, 100):
                c = (a + b) / 2
                error = abs(c - prev_c)
                rel_error = error / abs(c) if c != 0 else 0

                data.append([i, c, f(c), error, rel_error])

                if error < tol:
                    break

                if f(a) * f(c) < 0:
                    b = c
                else:
                    a = c

                prev_c = c

            st.success(f"Root ≈ {round(c,6)}")
            st.write("### Iteration Table")
            st.table(data)

# ---------- NEWTON ----------
if method == "Newton-Raphson":
    x = st.number_input("Initial Guess", value=1.5)

    if st.button("Calculate"):
        data = []

        def df(x):
            h = 1e-6
            return (f(x+h) - f(x-h)) / (2*h)

        for i in range(1, 100):
            if df(x) == 0:
                st.error("Derivative became zero")
                break

            x1 = x - f(x)/df(x)
            error = abs(x1 - x)
            rel_error = error / abs(x1) if x1 != 0 else 0

            data.append([i, x1, f(x1), error, rel_error])

            if error < tol:
                break

            x = x1

        st.success(f"Root ≈ {round(x1,6)}")
        st.write("### Iteration Table")
        st.table(data)
