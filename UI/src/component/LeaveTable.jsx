import { useEffect, useState } from "react";
import axios from "axios";

export default function LeaveTable() {
  const [leaveData, setLeaveData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaveData = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://localhost:8000/leave-applications", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setLeaveData(response.data);
      } catch (err) {
        console.error("Failed to fetch leave data", err);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaveData();
  }, []);

  if (loading) {
    return <div>Loading leave data...</div>;
  }

  return (
    <div style={{ marginTop: "2rem" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#f2f2f2" }}>
            <th style={tableHeaderStyle}>ID</th>
            <th style={tableHeaderStyle}>Employee</th>
            <th style={tableHeaderStyle}>Leave Type</th>
            <th style={tableHeaderStyle}>Start Date</th>
            <th style={tableHeaderStyle}>End Date</th>
            <th style={tableHeaderStyle}>Status</th>
          </tr>
        </thead>
        <tbody>
          {leaveData.map((leave) => (
            <tr key={leave.id} style={tableRowStyle}>
              <td style={tableCellStyle}>{leave.id}</td>
              <td style={tableCellStyle}>{leave.employee_id}</td>
              <td style={tableCellStyle}>{leave.leave_type_id}</td>
              <td style={tableCellStyle}>
                {new Date(leave.start_date).toLocaleDateString()}
              </td>
              <td style={tableCellStyle}>
                {new Date(leave.end_date).toLocaleDateString()}
              </td>
              <td style={tableCellStyle}>{leave.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const tableHeaderStyle = {
  padding: "12px",
  textAlign: "left",
  borderBottom: "1px solid #ddd",
};

const tableRowStyle = {
  borderBottom: "1px solid #ddd",
  ":hover": {
    backgroundColor: "#f5f5f5",
  },
};

const tableCellStyle = {
  padding: "12px",
  textAlign: "left",
};