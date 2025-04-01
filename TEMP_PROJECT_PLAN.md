User defined edits and features:
 - Fix the UI so that the top bar on the website is the same across the entire top, both in the page and the side pannel.
 - Edit the side pannel so that it contains the following items:
   - Dashboard
   - Tickets
   - Customers
   - Bikes
   - Parts
   - Settings
 - On the dashboard, fix the active tickets to show the number of active tickets accurately.
  - Change the website theme to a dark gray theme for dark mode instead of blue
  - Add a light theme with a toggle button.

## Agent Plan

### 1. Unify Top Bar and Sidebar Top Styling
*   **Goal:** Ensure the main top navigation bar and the top section of the sidebar have a consistent visual appearance (background, height, etc.).
*   **Files to Inspect/Modify:**
    *   `frontend/src/components/layout/MainLayout.tsx` (Primary target)
    *   Potentially a separate Sidebar component if imported by `MainLayout.tsx`.
    *   `frontend/tailwind.config.js` (If custom theme colors/heights are involved)
    *   `frontend/src/index.css` (For global styles or CSS variables)
*   **Steps:**
    1.  **Locate Components:** Identify the JSX elements rendering the top navigation bar and the sidebar within `MainLayout.tsx`.
    2.  **Analyze Styles:** Use browser developer tools and inspect the code to find the Tailwind classes or CSS rules responsible for the background color, height, padding, borders, and shadows of both elements. Note the differences.
    3.  **Apply Consistent Styles:** Modify the Tailwind classes directly in the JSX. Choose a consistent background color (e.g., `bg-gray-100 dark:bg-gray-800`), height (e.g., `h-16`), padding (e.g., `px-4 py-2`), and remove or unify any borders/shadows causing visual separation. Ensure vertical alignment if necessary.
    4.  **Verify:** Run `npm run dev --prefix frontend`. Check multiple pages (Dashboard, Ticket List, etc.) in both light and dark modes (once implemented) to confirm the top area looks unified.

### 2. Update Sidebar Navigation Links
*   **Goal:** Modify the sidebar to display links for Dashboard, Tickets, Customers, Bikes, Parts, and Settings.
*   **Files to Inspect/Modify:**
    *   `frontend/src/components/layout/MainLayout.tsx` (Or a dedicated Sidebar component)
    *   `frontend/src/App.tsx` (To verify/add routes)
*   **Steps:**
    1.  **Locate Nav Structure:** Find the list or container rendering the navigation links (likely using `NavLink` from `react-router-dom`) within the sidebar component.
    2.  **Map Links:** Create an array or structure defining the desired links, their text, target route (`to` prop), and potentially an icon.
        ```javascript
        // Example structure (actual icons need importing/defining)
        const navLinks = [
          { text: 'Dashboard', to: '/', icon: <DashboardIcon /> },
          { text: 'Tickets', to: '/tickets', icon: <TicketIcon /> },
          { text: 'Customers', to: '/customers', icon: <CustomerIcon /> }, // Assuming route exists
          { text: 'Bikes', to: '/bikes', icon: <BikeIcon /> },         // Assuming route exists
          { text: 'Parts', to: '/parts', icon: <PartIcon /> },         // Assuming route exists
          { text: 'Settings', to: '/settings', icon: <SettingsIcon /> }, // May need new route/page
        ];
        ```
    3.  **Render Links:** Replace the existing link rendering logic with a map over the `navLinks` array, generating a `NavLink` for each item. Apply appropriate styling for active/inactive states.
    4.  **Add Routes (If Needed):** Check `frontend/src/App.tsx`. If routes like `/customers`, `/bikes`, `/parts`, or `/settings` don't exist, add basic placeholder routes and components for them.
    5.  **Verify:** Run `npm run dev --prefix frontend`. Check if all links appear correctly in the sidebar. Click each link to ensure it navigates to the correct page (or placeholder). Check active link styling.

### 3. Fix Active Tickets Count on Dashboard
*   **Goal:** Display the correct number of tickets that are not 'Closed' and not 'Archived' on the dashboard.
*   **Files to Inspect/Modify:**
    *   `frontend/src/pages/Dashboard.tsx`
    *   `frontend/src/services/ticket-service.ts`
    *   `backend/app/api/endpoints/tickets.py` (Specifically the `read_tickets` function or similar)
    *   `backend/app/models/ticket.py` (To confirm status values and `is_archived` field)
    *   `backend/app/schemas/ticket.py` (To confirm fields in API response)
*   **Steps:**
    1.  **Frontend - Data Fetching:** In `Dashboard.tsx`, find how ticket data is fetched (likely using a function from `ticket-service.ts`).
    2.  **Backend - Check Filtering:** In `tickets.py`, examine the `GET /tickets` endpoint. Does it already support filtering by status (e.g., `?status=Open&status=In%20Progress`) or by an `is_archived` flag? Does it exclude archived tickets by default? What are the exact status strings defined in `models/ticket.py`? (Assume 'Closed' is the status to exclude, and check for an `is_archived` boolean field).
    3.  **Backend - Modify Endpoint (If Needed):**
        *   If filtering is insufficient, update the SQLAlchemy query in the `read_tickets` function (or equivalent) in `tickets.py` to filter out tickets where `status == 'Closed'` and where `is_archived == True`. Consider adding specific query parameters like `?active=true` or adjust the default behavior to return only active tickets unless otherwise specified.
        *   Ensure the `TicketRead` schema (`schemas/ticket.py`) includes the `status` and `is_archived` fields if they are needed for frontend filtering.
    4.  **Frontend - Update Service Call:** Modify the function in `ticket-service.ts` that the dashboard uses. If the backend now supports filtering (e.g., `?active=true`), add that parameter to the API call.
    5.  **Frontend - Update Dashboard Component:**
        *   If the service call now returns only active tickets, display the `length` of the returned array.
        *   If the service call still returns all tickets (and includes `status` and `is_archived`), filter the array in the component: `const activeTickets = tickets.filter(t => t.status !== 'Closed' && !t.is_archived);`. Display `activeTickets.length`. Choose the most efficient approach (backend filtering is generally preferred).
    6.  **Verify:** Run both backend and frontend. Use tools like `add_test_data.py` or manually create tickets with 'Open', 'In Progress', 'Closed' statuses. Archive some tickets via the API or database. Check if the count on the dashboard accurately reflects only the non-closed, non-archived tickets.

### 4. Implement Dark Gray Dark Mode Theme
*   **Goal:** Change the dark mode color scheme from the current blue-based theme to a dark gray-based theme.
*   **Files to Inspect/Modify:**
    *   `frontend/tailwind.config.js`
    *   `frontend/src/index.css` (Less likely, but possible for CSS variables)
    *   Various components applying `dark:` variants (e.g., `MainLayout.tsx`, `Button.tsx`, `Card.tsx`).
*   **Steps:**
    1.  **Check Tailwind Config:** Open `frontend/tailwind.config.js`. Confirm `darkMode: 'class'` is present. Examine the `theme.extend.colors` section for custom blue or gray definitions used in dark mode.
    2.  **Define Gray Palette:** Ensure Tailwind's default grays (`colors.gray`) are sufficient or define custom dark gray shades if needed in `theme.extend.colors`.
    3.  **Search and Replace:** Search the `frontend/src` directory for Tailwind classes using `dark:bg-blue-`, `dark:text-blue-`, `dark:border-blue-`, `dark:hover:bg-blue-`, etc.
    4.  **Apply Gray Styles:** Replace the found blue classes with corresponding gray classes (e.g., replace `dark:bg-blue-700` with `dark:bg-gray-800`, `dark:text-blue-100` with `dark:text-gray-100`, `dark:border-blue-500` with `dark:border-gray-600`). Pay attention to shades to maintain contrast and visual hierarchy. Update primary buttons, backgrounds, text colors, borders, hover states, etc.
    5.  **Check Global Styles:** Look in `index.css` for any `:root.dark` or `[data-theme='dark']` rules setting blue colors via CSS variables and update them to use grays.
    6.  **Verify:** Run `npm run dev --prefix frontend`. Ensure dark mode is active (via toggle or system preference). Visually inspect all pages and components (buttons, cards, forms, layout) to confirm the blue theme is replaced by dark gray. Check for readability and contrast issues.

### 5. Add Light/Dark Theme Toggle
*   **Goal:** Introduce a light theme and a button to switch between light and dark modes, persisting the choice.
*   **Files to Create/Modify:**
    *   `frontend/src/contexts/ThemeContext.tsx` (New file)
    *   `frontend/src/components/ui/ThemeToggle.tsx` (New file)
    *   `frontend/src/main.tsx` (To wrap app with ThemeProvider)
    *   `frontend/src/components/layout/MainLayout.tsx` (To place the toggle button)
    *   `frontend/tailwind.config.js` (Ensure `darkMode: 'class'`)
*   **Steps:**
    1.  **Confirm Tailwind Dark Mode Strategy:** Verify `darkMode: 'class'` is set in `tailwind.config.js`.
    2.  **Create Theme Context:**
        *   Create `frontend/src/contexts/ThemeContext.tsx`.
        *   Use `React.createContext`, `useState`, and `useEffect`.
        *   Initialize theme state by reading from `localStorage.getItem('theme')` (e.g., 'light' or 'dark'). Fallback to 'light' or system preference (`window.matchMedia('(prefers-color-scheme: dark)').matches`).
        *   Create a `setTheme` function that updates the state, writes to `localStorage.setItem('theme', newTheme)`, and adds/removes the 'dark' class on `document.documentElement`.
        *   Provide the current `theme` and `setTheme` function via the context provider.
    3.  **Wrap Application:** In `frontend/src/main.tsx`, import `ThemeProvider` from your context and wrap the `<App />` component with it.
    4.  **Create Toggle Button Component:**
        *   Create `frontend/src/components/ui/ThemeToggle.tsx`.
        *   Use `useContext` to access the `theme` and `setTheme` function from `ThemeContext`.
        *   Render a button. Display a sun icon (e.g., from `react-icons/fi`) if `theme === 'dark'` and a moon icon if `theme === 'light'`.
        *   Set the button's `onClick` handler to call `setTheme(theme === 'light' ? 'dark' : 'light')`.
    5.  **Place Toggle Button:** Import and render the `<ThemeToggle />` component within `frontend/src/components/layout/MainLayout.tsx`, likely in the top navigation bar area.
    6.  **Define Light Theme Styles (Review):** Tailwind's default styles usually form the basis of the light theme when `darkMode: 'class'` is used. Review components to ensure text is dark on light backgrounds and contrast is adequate. Remove any hardcoded dark styles that *don't* use the `dark:` prefix. Ensure base background/text colors are set appropriately in `index.css` or the main layout for the default (light) theme.
    7.  **Verify:** Run `npm run dev --prefix frontend`. Find the toggle button. Click it to switch between themes. Check if the UI updates correctly (colors, backgrounds, text). Refresh the page – the selected theme should persist due to localStorage. Check appearance and readability in both modes across different pages.
