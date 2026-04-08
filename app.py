import streamlit as st
import math

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
    "Regula Falsi",
    "Trapezoidal Rule",
    "Simpson's Rule",
    "Numerical Differentiation"
])

tol = st.number_input("Tolerance", value=0.0001, format="%.6f")

# ================= ROOT FINDING =================

# ---------- BISECTION ----------
if method == "Bisection":
    a = st.number_input("a", value=1.0)
    b = st.number_input("b", value=2.0)

    if st.button("Calculate"):
        if f(a)*f(b) >= 0:
            st.error("Invalid interval")
        else:
            data = []
            prev_c = a

            for i in range(1, 100):
                c = (a + b)/2
                error = abs(c - prev_c)
                rel_error = error/abs(c) if c != 0 else 0

                data.append([i, c, f(c), error, rel_error])

                if error < tol:
                    break

                if f(a)*f(c) < 0:
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
                st.error("Derivative = 0")
                break

            x1 = x - f(x)/df(x)
            error = abs(x1 - x)
            rel_error = error/abs(x1) if x1 != 0 else 0

            data.append([i, x1, f(x1), error, rel_error])

            if error < tol:
                break

            x = x1

        st.success(f"Root ≈ {round(x1,6)}")
        st.write("### Iteration Table")
        st.table(data)

# ---------- SECANT ----------
if method == "Secant":
    x0 = st.number_input("x0", value=1.0)
    x1 = st.number_input("x1", value=2.0)

    if st.button("Calculate"):
        data = []

        for i in range(1, 100):
            if f(x1) - f(x0) == 0:
                st.error("Division by zero")
                break

            x2 = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
            error = abs(x2 - x1)
            rel_error = error/abs(x2) if x2 != 0 else 0

            data.append([i, x2, f(x2), error, rel_error])

            if error < tol:
                break

            x0, x1 = x1, x2

        st.success(f"Root ≈ {round(x2,6)}")
        st.write("### Iteration Table")
        st.table(data)

# ---------- REGULA FALSI ----------
if method == "Regula Falsi":
    a = st.number_input("a", value=1.0)
    b = st.number_input("b", value=2.0)

    if st.button("Calculate"):
        if f(a)*f(b) >= 0:
            st.error("Invalid interval")
        else:
            data = []
            prev_c = a

            for i in range(1, 100):
                c = (a*f(b) - b*f(a)) / (f(b) - f(a))
                error = abs(c - prev_c)
                rel_error = error/abs(c) if c != 0 else 0

                data.append([i, c, f(c), error, rel_error])

                if error < tol:
                    break

                if f(a)*f(c) < 0:
                    b = c
                else:
                    a = c

                prev_c = c

            st.success(f"Root ≈ {round(c,6)}")
            st.write("### Iteration Table")
            st.table(data)

# ================= INTEGRATION =================

# ---------- TRAPEZOIDAL ----------
if method == "Trapezoidal Rule":
    a = st.number_input("Lower limit", value=0.0)
    b = st.number_input("Upper limit", value=1.0)
    n = st.number_input("Intervals (n)", value=4)

    if st.button("Calculate"):
        h = (b - a) / n
        s = 0.5*(f(a) + f(b))

        for i in range(1, int(n)):
            s += f(a + i*h)

        result = h * s
        st.success(f"Integral ≈ {round(result,6)}")

# ---------- SIMPSON ----------
if method == "Simpson's Rule":
    a = st.number_input("Lower limit", value=0.0)
    b = st.number_input("Upper limit", value=1.0)
    n = st.number_input("Even intervals (n)", value=4)

    if n % 2 != 0:
        st.warning("n must be even")

    if st.button("Calculate"):
        h = (b - a) / n
        s = f(a) + f(b)

        for i in range(1, int(n)):
            if i % 2 == 0:
                s += 2*f(a + i*h)
            else:
                s += 4*f(a + i*h)

        result = (h/3)*s
        st.success(f"Integral ≈ {round(result,6)}")

# ================= DIFFERENTIATION =================

# ---------- NUMERICAL DIFFERENTIATION ----------
if method == "Numerical Differentiation":
    x = st.number_input("Point x", value=1.0)
    h = st.number_input("Step size h", value=0.001)

    if st.button("Calculate"):
        forward = (f(x+h) - f(x)) / h
        backward = (f(x) - f(x-h)) / h
        central = (f(x+h) - f(x-h)) / (2*h)

        st.write(f"Forward Difference: {round(forward,6)}")
        st.write(f"Backward Difference: {round(backward,6)}")
        st.write(f"Central Difference: {round(central,6)}")
