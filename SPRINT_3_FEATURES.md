# 🎉 Sprint 3 New Features - Quick Guide

**Date:** February 10, 2025  
**Status:** ✅ All Features Complete

---

## 🚀 How to See the New Features

### 1. Start the Application

**Backend:**
```powershell
# In terminal 1
.\run-backend.ps1

# Or with Docker
docker-compose up backend postgres redis -d
```

**Frontend:**
```powershell
# In terminal 2
.\run-dashboard.ps1

# Or manually
cd apps/dashboard
npm run dev
```

**Open:** http://localhost:3000

---

## ✨ New Features

### 📈 1. Interactive Price Chart

**Location:** Below the price card on the dashboard

**Features to Try:**
- ✅ Click the **[24h]**, **[7d]**, or **[30d]** buttons to change time range
- ✅ Hover over the chart to see detailed price tooltips
- ✅ View price statistics at the bottom (High, Low, Average, Data Points)
- ✅ Watch the price change indicator (▲/▼) with percentage

**Expected Behavior:**
- Chart updates smoothly when changing time ranges
- Tooltips show exact price and timestamp on hover
- Golden/amber line represents gold price (XAUUSD)

---

### 📊 2. Sentiment Trend Chart

**Location:** Below the price chart

**Features to Try:**
- ✅ Switch between **[24h]**, **[7d]**, **[30d]** time ranges
- ✅ Hover to see sentiment scores and article counts
- ✅ View sentiment distribution (Positive/Neutral/Negative percentages)
- ✅ Check reference lines at ±0.3 (Bullish/Bearish zones)

**Expected Behavior:**
- Area chart with gradient (green = positive, red = negative)
- Sentiment label updates (Bullish/Neutral/Bearish)
- Distribution cards show percentage breakdown

---

### 🔔 3. Alert Management Panel

**Location:** Below the sentiment chart

**Features to Try:**

**Creating Alerts:**
1. Click **[Create Alert]** button
2. Select alert type (Price Threshold, Price Change, Sentiment Shift, etc.)
3. Choose severity (Low, Medium, High, Critical)
4. Enter threshold value
5. Add optional custom message
6. Click **[Create Alert]**

**Managing Alerts:**
- ✅ Filter by severity using buttons (All, Critical, High, Medium, Low)
- ✅ Click **✓** to acknowledge an alert
- ✅ Click **✕** to delete an alert
- ✅ Alerts auto-refresh every 30 seconds

**Expected Behavior:**
- Alerts display with color-coded severity badges
- Icons indicate alert type (price/sentiment)
- Modal form validates input before submission

---

### 🌓 4. Dark/Light Mode Toggle

**Location:** Top-right corner of the header (next to API Docs button)

**Features to Try:**
- ✅ Click the toggle to switch between light and dark mode
- ✅ Watch all components transition smoothly
- ✅ Theme persists after page reload
- ✅ Matches system preference by default

**Expected Behavior:**
- ☀️ Sun icon in light mode
- 🌙 Moon icon in dark mode
- Smooth transitions (no flicker)
- All charts, cards, and text adapt to theme

---

## 🎨 Visual Examples

### Light Mode
```
┌─────────────────────────────────────────────┐
│  AUREX.AI                    [☀️] [API Docs] │  ← Toggle here
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  XAUUSD: $2,805.50  ▲ $15.23 (+0.55%)      │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  📈 Price History      [24h] [7d] [30d]    │  ← New Chart
│  ╭──────────────────────────────────╮      │
│  │      Price Line Chart             │      │
│  ╰──────────────────────────────────╯      │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  📊 Sentiment Trend    [24h] [7d] [30d]    │  ← New Chart
│  ╭──────────────────────────────────╮      │
│  │      Sentiment Area Chart         │      │
│  ╰──────────────────────────────────╯      │
└─────────────────────────────────────────────┘
┌─────────────────────────────────────────────┐
│  🔔 Alerts            [Create Alert]       │  ← New Panel
│  [All] [Critical] [High] [Medium] [Low]    │
│  ╭──────────────────────────────────╮      │
│  │ 🔴 CRITICAL - Price Alert         │      │
│  │ Price above $2,800                │      │
│  ╰──────────────────────────────────╯      │
└─────────────────────────────────────────────┘
```

### Dark Mode
- Same layout, but with dark backgrounds
- White/light gray text
- Adjusted chart colors for contrast

---

## 🧪 Testing Checklist

### Price Chart
- [ ] Load page and verify chart displays
- [ ] Click [24h] - chart updates
- [ ] Click [7d] - chart updates
- [ ] Click [30d] - chart updates
- [ ] Hover over chart - tooltip appears
- [ ] Check stats footer has values

### Sentiment Chart
- [ ] Chart displays with gradient
- [ ] Time range buttons work
- [ ] Hover shows sentiment details
- [ ] Distribution cards show percentages
- [ ] Reference lines visible at ±0.3

### Alert Panel
- [ ] Click [Create Alert] - modal opens
- [ ] Fill form and submit - alert created
- [ ] Filter by severity - alerts filter
- [ ] Click ✓ on alert - acknowledges
- [ ] Click ✕ on alert - deletes (with confirmation)
- [ ] Wait 30s - panel auto-refreshes

### Dark Mode
- [ ] Click toggle - switches to dark
- [ ] All components are visible in dark mode
- [ ] Toggle back - switches to light
- [ ] Reload page - theme persists
- [ ] Charts render correctly in both themes

---

## 🐛 Troubleshooting

### Charts Not Showing Data

**Problem:** Charts show "No data available"

**Solutions:**
1. Make sure the backend is running (`http://localhost:8000/docs`)
2. Check if database has data:
   ```powershell
   docker-compose exec postgres psql -U aurex -d aurex_db
   # In psql:
   SELECT COUNT(*) FROM price;
   SELECT COUNT(*) FROM sentiment_summary;
   ```
3. Run the pipeline to fetch data:
   ```powershell
   cd apps/pipeline
   python -m apps.pipeline.tasks.fetch_price
   python -m apps.pipeline.tasks.fetch_news
   ```

### Alerts Not Creating

**Problem:** "Create Alert" fails with error

**Solutions:**
1. Verify backend is running
2. Check browser console for errors (F12 → Console)
3. Test API directly: `http://localhost:8000/api/v1/alerts`
4. Ensure database connection is working

### Theme Toggle Not Working

**Problem:** Toggle doesn't switch themes

**Solutions:**
1. Clear browser cache and reload
2. Check browser console for errors
3. Verify `localStorage` is enabled
4. Try incognito/private mode

### Charts Loading Forever

**Problem:** Spinner shows indefinitely

**Solutions:**
1. Check network tab (F12 → Network) for failed requests
2. Verify API endpoints respond: `/api/v1/price/history`, `/api/v1/sentiment/history`
3. Check CORS errors in console
4. Ensure backend has CORS enabled for `http://localhost:3000`

---

## 📊 Expected Performance

| Feature | Load Time | Update Time |
|---------|-----------|-------------|
| Price Chart | <1 second | <200ms |
| Sentiment Chart | <1 second | <200ms |
| Alert Panel | <500ms | <100ms |
| Theme Toggle | Instant | <50ms |

---

## 🎯 What's Next?

After testing Sprint 3 features, we can proceed to:

### Sprint 4: Deployment & Advanced Features

**Deployment:**
- Deploy backend to Railway
- Deploy frontend to Vercel
- Configure production environment variables
- Set up monitoring and logging

**Advanced Features:**
- WebSocket for real-time updates
- Price prediction model
- Advanced analytics
- User authentication

**Testing & Quality:**
- Write automated tests
- Set up CI/CD pipeline
- Code coverage reports
- Performance optimization

---

## 💡 Tips for Best Experience

1. **Use Real Data:** Run the pipeline to fetch live gold prices and news
2. **Test Both Themes:** Try the dashboard in light and dark mode
3. **Create Test Alerts:** Set up various alerts to see the system in action
4. **Try Different Time Ranges:** Compare 24h vs 7d vs 30d views
5. **Check Responsiveness:** Resize browser window to see responsive design

---

## 📸 Screenshots

Take screenshots and share feedback!

**Recommended Views:**
- Full dashboard in light mode
- Full dashboard in dark mode
- Price chart with tooltip visible
- Sentiment chart with distribution
- Alert panel with multiple alerts
- Alert creation modal

---

## 📞 Need Help?

**Check:**
- `START-HERE.md` - Quick start guide
- `QUICKSTART.md` - Detailed setup
- `docs/SPRINT_3_COMPLETE.md` - Full technical report

**Issues?**
- Check browser console (F12)
- Check backend logs
- Verify Docker services are running
- Review `docker-compose ps` output

---

**Enjoy the new features!** 🎉

✨ **AUREX.AI - Advanced Financial Intelligence** ✨

