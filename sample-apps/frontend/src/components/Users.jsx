import { useState, useEffect } from 'react'
import './Users.css'

function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [newUser, setNewUser] = useState({ name: '', email: '', role: 'user' })

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/v1/users')
      const data = await response.json()
      setUsers(data.users || [])
      setError(null)
    } catch (err) {
      setError('Failed to fetch users. Make sure backend API is running on port 3000.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateUser = async (e) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newUser),
      })

      if (response.ok) {
        setNewUser({ name: '', email: '', role: 'user' })
        fetchUsers()
      }
    } catch (err) {
      console.error('Error creating user:', err)
    }
  }

  if (loading) return <div className="loading">Loading users...</div>
  if (error) return <div className="error">{error}</div>

  return (
    <div className="Users">
      <h2>User Management</h2>
      <p className="subtitle">Backend API (Node.js + Express)</p>

      <div className="user-grid">
        <div className="user-list">
          <h3>Current Users ({users.length})</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className={`badge ${user.role}`}>{user.role}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="user-form">
          <h3>Create New User</h3>
          <form onSubmit={handleCreateUser}>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={newUser.name}
                onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                required
              />
            </div>

            <div className="form-group">
              <label>Role</label>
              <select
                value={newUser.role}
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>

            <button type="submit" className="btn-primary">Create User</button>
          </form>

          <div className="api-info">
            <h4>API Endpoint</h4>
            <code>POST /api/v1/users</code>
            <p>Backend running on port 3000</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Users
