document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const message = document.getElementById("dashboard-message");
  const revenue = document.getElementById("revenue-amount");
  const expenses = document.getElementById("expenses-amount");
  const profit = document.getElementById("profit-amount");

  const chartCanvas = document.getElementById("finance-chart");
  let financeChart = null;

  const showModal = document.getElementById("add-transaction-btn");
  const modal = document.getElementById("transaction-modal");
  const closeModal = document.getElementById("close-modal");
  const form = document.getElementById("transaction-form");

  const showFeedback = (msg, type = "success") => {
    let feedback = document.getElementById("feedback");
    if (!feedback) {
      feedback = document.createElement("div");
      feedback.id = "feedback";
      feedback.className = "feedback-message";
      form.appendChild(feedback);
    }
    feedback.textContent = msg;
    feedback.className = `feedback-message ${type}`;
    feedback.style.display = "block";
    setTimeout(() => {
      feedback.style.display = "none";
    }, 3000);
  };
  console.log("📦 Sending token:", token);

  const fetchDashboard = async () => {
    if (!token) {
      console.warn("❌ No token found, redirecting...");
      window.location.href = "/login";
      return;
    }

    try {
      const res = await fetch("/api/dashboard-data", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (!res.ok) {
        console.error("🚫 Invalid token or session expired.");
        throw new Error("Unauthorized");
      }

      const data = await res.json();
      console.log("✅ Dashboard data:", data);

      message.textContent = `Welcome back, ${data.email}!`;

      const income = data.income || 0;
      const expense = data.expense || 0;
      const net = income - expense;

      revenue.textContent = `$${income.toFixed(2)}`;
      expenses.textContent = `$${expense.toFixed(2)}`;
      profit.textContent = `$${net.toFixed(2)}`;

      if (financeChart) financeChart.destroy();

      financeChart = new Chart(chartCanvas, {
        type: "doughnut",
        data: {
          labels: ["Income", "Expenses"],
          datasets: [
            {
              label: "Finances",
              data: [income, expense],
              backgroundColor: ["#4caf50", "#f44336"],
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "bottom"
            }
          }
        }
      });
    } catch (err) {
      console.error("🔥 Error fetching dashboard data:", err);
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  };

  fetchDashboard();

  showModal?.addEventListener("click", () => modal?.classList.remove("hidden"));
  closeModal?.addEventListener("click", () => modal?.classList.add("hidden"));

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const type = form.type.value;
    const amount = parseFloat(form.amount.value);
    const category = form.category.value;
    const note = form.note.value;

    if (!amount || isNaN(amount)) {
      showFeedback("Please enter a valid amount.", "error");
      return;
    }

    try {
      const res = await fetch("/transactions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ type, amount, category, note })
      });

      const result = await res.json();

      if (res.ok) {
        showFeedback("✅ Transaction added!", "success");
        form.reset();
        modal.classList.add("hidden");
        fetchDashboard();
      } else {
        showFeedback(result.error || "Failed to add transaction.", "error");
      }
    } catch (err) {
      showFeedback("Server error. Please try again.", "error");
    }
  });
});
