import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Scientific Calculator", layout="centered")
st.title("🔬 Scientific Calculator with Error Analysis")

# ---------- FUNCTION ----------
func_str = st.text_input("Enter function f(x):", "x**3 - x - 2")

def f(x):
    try:
        return eval(func_str)
    except:
        return None

method = st.selectbox("Select Method", [
    "Bisection",
    "Newton-Raphson",
    "Secant",
    "Regula Falsi"
])

tol = st.number_input("Tolerance", value=0.0001, format="%.6f")
true_root = st.text_input("Exact Root (optional)")

# ---------- GRAPH ----------
def plot_function(root=None):
    x_vals = np.linspace(-10, 10, 400)
    y_vals = [f(x) for x in x_vals]

    plt.figure()
    plt.axhline(0)
    plt.plot(x_vals, y_vals)

    if root is not None:
        plt.scatter(root, f(root))

    st.pyplot(plt)

# ---------- RESULT DISPLAY ----------
def show_results(data, root):
    st.success(f"Root ≈ {round(root,6)}")

    # Create DataFrame with headings
    columns = ["Iter", "x", "f(x)", "Abs Error", "Rel Error", "Theoretical Error", "True Error"]
    df = pd.DataFrame(data, columns=columns)

    st.write("### 📊 Iteration Table with Error Types")
    st.dataframe(df)

    # Convergence graph
    plt.figure()
    plt.plot(df["Abs Error"])
    plt.title("📉 Approximate Error Convergence")
    plt.xlabel("Iteration")
    plt.ylabel("Absolute Error")
    st.pyplot(plt)

    plot_function(root)

    # ---------- TRUE ERROR GRAPH ----------
    if true_root:
        try:
            true_val = float(true_root)

            plt.figure()
            plt.plot(df["True Error"], label="True Error")

            if "Theoretical Error" in df.columns:
                plt.plot(df["Theoretical Error"], label="Theoretical Error")

            plt.legend()
            plt.title("📊 Error Comparison (True vs Theoretical)")
            st.pyplot(plt)

            final_true_error = abs(true_val - root)
            percent_error = (final_true_error / abs(true_val)) * 100

            st.write(f"### ✅ Final True Error: {final_true_error}")
            st.write(f"### ✅ Percentage Error: {percent_error}%")

        except:
            st.warning("Invalid exact root input")

# ================= BISECTION =================
if method == "Bisection":
    a = st.number_input("a", value=1.0)
    b = st.number_input("b", value=2.0)

    if st.button("Calculate"):
        data = []
        prev_c = a

        for i in range(1, 100):
            c = (a + b)/2
            error = abs(c - prev_c)
            rel_error = error/abs(c) if c != 0 else 0
            theoretical_error = (b - a)/(2**i)
            true_err = abs(float(true_root) - c) if true_root else None

            data.append([i, c, f(c), error, rel_error, theoretical_error, true_err])

            if error < tol:
                break

            if f(a)*f(c) < 0:
                b = c
            else:
                a = c

            prev_c = c

        show_results(data, c)

# ================= NEWTON =================
if method == "Newton-Raphson":
    x = st.number_input("Initial Guess", value=1.5)

    if st.button("Calculate"):
        data = []

        def df(x):
            h = 1e-6
            return (f(x+h) - f(x-h)) / (2*h)

        for i in range(1, 100):
            x1 = x - f(x)/df(x)
            error = abs(x1 - x)
            rel_error = error/abs(x1) if x1 != 0 else 0
            true_err = abs(float(true_root) - x1) if true_root else None

            data.append([i, x1, f(x1), error, rel_error, None, true_err])

            if error < tol:
                break

            x = x1

        show_results(data, x1)

# ================= SECANT =================
if method == "Secant":
    x0 = st.number_input("x0", value=1.0)
    x1 = st.number_input("x1", value=2.0)

    if st.button("Calculate"):
        data = []

        for i in range(1, 100):
            x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
            error = abs(x2 - x1)
            rel_error = error/abs(x2) if x2 != 0 else 0
            true_err = abs(float(true_root) - x2) if true_root else None

            data.append([i, x2, f(x2), error, rel_error, None, true_err])

            if error < tol:
                break

            x0, x1 = x1, x2

        show_results(data, x2)

# ================= REGULA FALSI =================
if method == "Regula Falsi":
    a = st.number_input("a", value=1.0)
    b = st.number_input("b", value=2.0)

    if st.button("Calculate"):
        data = []
        prev_c = a

        for i in range(1, 100):
            c = (a*f(b) - b*f(a))/(f(b)-f(a))
            error = abs(c - prev_c)
            rel_error = error/abs(c) if c != 0 else 0
            true_err = abs(float(true_root) - c) if true_root else None

            data.append([i, c, f(c), error, rel_error, None, true_err])

            if error < tol:
                break

            if f(a)*f(c) < 0:
                b = c
            else:
                a = c

            prev_c = c

        show_results(data, c)
