(() => {
  "use strict";

  let staffKey = "";
  let selectedTicketId = "";

  const $ = (id) => document.getElementById(id);
  const loginCard = $("login-card");
  const workspace = $("workspace");
  const loginError = $("login-error");
  const workspaceError = $("workspace-error");
  const statusLabels = {
    waiting_human: "待人工处理",
    processing: "处理中",
    resolved: "已解决",
  };

  function showError(target, message) {
    target.textContent = message;
    target.hidden = false;
  }

  function clearError(target) {
    target.textContent = "";
    target.hidden = true;
  }

  async function api(path, options = {}) {
    const headers = new Headers(options.headers || {});
    headers.set("X-Staff-Key", staffKey);
    if (options.body) headers.set("Content-Type", "application/json");
    const response = await fetch(path, { ...options, headers, cache: "no-store" });
    if (response.status === 401) {
      disconnect("访问密钥无效或已过期，请重新输入。");
      throw new Error("访问密钥无效或已过期。");
    }
    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      throw new Error(payload.detail || "请求失败，请稍后重试。");
    }
    return response.json();
  }

  function disconnect(message = "") {
    staffKey = "";
    selectedTicketId = "";
    workspace.hidden = true;
    $("ticket-detail").hidden = true;
    $("disconnect-button").hidden = true;
    loginCard.hidden = false;
    if (message) showError(loginError, message);
    $("staff-key").focus();
  }

  function setMetric(id, value) {
    $(id).textContent = String(value ?? 0);
  }

  async function loadSummary() {
    const summary = await api("/internal/audit-events/summary?minutes=60");
    setMetric("metric-total", summary.totalRequests);
    setMetric("metric-completed", summary.completedRequests);
    setMetric("metric-failed", summary.failedRequests);
    setMetric("metric-rate-limited", summary.rateLimitedRequests);
  }

  function ticketMeta(ticket) {
    const user = ticket.userId == null ? "未关联用户" : `用户 ${ticket.userId}`;
    return `${user} · ${ticket.createdAt}`;
  }

  async function loadTickets() {
    const ticketList = $("ticket-list");
    ticketList.replaceChildren();
    const filter = $("ticket-status").value;
    const tickets = await api(`/internal/tickets?status=${encodeURIComponent(filter)}&limit=100`);
    $("ticket-caption").textContent = `共 ${tickets.length} 条${statusLabels[filter]}工单`;
    if (!tickets.length) {
      const empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = "暂无工单。";
      ticketList.append(empty);
      return;
    }
    tickets.forEach((ticket) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "ticket";
      button.addEventListener("click", () => {
        loadTicket(ticket.ticketId).catch((error) => {
          if (staffKey) showError(workspaceError, error.message);
        });
      });

      const content = document.createElement("div");
      const question = document.createElement("p");
      question.className = "ticket-title";
      question.textContent = ticket.question;
      const meta = document.createElement("p");
      meta.className = "ticket-meta";
      meta.textContent = `${ticket.ticketId} · ${ticketMeta(ticket)}`;
      content.append(question, meta);

      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = statusLabels[ticket.status] || ticket.status;
      button.append(content, badge);
      ticketList.append(button);
    });
  }

  function appendMetadata(ticket) {
    $("detail-ticket-id").textContent = ticket.ticketId;
    $("detail-status").textContent = statusLabels[ticket.status] || ticket.status;
    $("detail-user").textContent = ticket.userId == null ? "未关联用户" : `用户 ${ticket.userId}`;
    $("detail-created").textContent = ticket.createdAt;
    $("detail-handler").textContent = ticket.handledBy || "未分配";
    $("handled-by").value = ticket.handledBy || "";
  }

  function renderConversation(conversation) {
    const container = $("conversation");
    container.replaceChildren();
    conversation.forEach((message) => {
      const item = document.createElement("div");
      item.className = `message ${message.role === "assistant" ? "assistant" : "human"}`;
      const role = document.createElement("span");
      role.className = "message-role";
      role.textContent = message.role === "assistant" ? "智能客服" : "用户";
      const content = document.createElement("div");
      content.textContent = message.content;
      item.append(role, content);
      container.append(item);
    });
  }

  async function loadTicket(ticketId) {
    clearError(workspaceError);
    const ticket = await api(`/internal/tickets/${encodeURIComponent(ticketId)}`);
    selectedTicketId = ticket.ticketId;
    appendMetadata(ticket);
    renderConversation(ticket.conversation);
    $("ticket-detail").hidden = false;
    $("ticket-detail").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function refreshWorkspace() {
    clearError(workspaceError);
    await Promise.all([loadSummary(), loadTickets()]);
  }

  $("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    staffKey = $("staff-key").value.trim();
    clearError(loginError);
    if (!staffKey) return;
    try {
      await refreshWorkspace();
      if (!staffKey) return;
      $("staff-key").value = "";
      loginCard.hidden = true;
      workspace.hidden = false;
      $("disconnect-button").hidden = false;
    } catch (error) {
      showError(loginError, error.message);
    }
  });

  $("disconnect-button").addEventListener("click", () => disconnect());
  $("refresh-button").addEventListener("click", () => {
    refreshWorkspace().catch((error) => {
      if (staffKey) showError(workspaceError, error.message);
    });
  });
  $("ticket-status").addEventListener("change", async () => {
    $("ticket-detail").hidden = true;
    selectedTicketId = "";
    try {
      await refreshWorkspace();
    } catch (error) {
      if (staffKey) showError(workspaceError, error.message);
    }
  });

  $("ticket-update-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const action = event.submitter?.dataset.status;
    const handledBy = $("handled-by").value.trim();
    if (!selectedTicketId || !action || !handledBy) {
      showError(workspaceError, "请先填写处理人。");
      return;
    }
    clearError(workspaceError);
    try {
      await api(`/internal/tickets/${encodeURIComponent(selectedTicketId)}`, {
        method: "PATCH",
        body: JSON.stringify({ status: action, handledBy }),
      });
      await refreshWorkspace();
      await loadTicket(selectedTicketId);
    } catch (error) {
      if (staffKey) showError(workspaceError, error.message);
    }
  });
})();
