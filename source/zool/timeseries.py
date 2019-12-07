
class TimeSeriesTicks:
	def __init__(self, start_time, end_time, labels, fig):
		self._panel_labels = labels
		self._panel_bottom = labels[-1]
		self._start_time = start_time
		self._end_time = end_time
		self._width = fig['base'].width.value()
		self._fig = fig
		self._sec_per_cm = (end_time-start_time)/self._width
		self._ticks = None
		self._tick_labels = None
		self._minor_locator = None

		if self._sec_per_cm>(16*86400):
			# monthly ticks
			warnings.warn('Monthly ticks not yet implemented')
			pass
		elif self._sec_per_cm>(5*86400):
			# Ticks every 5 days, minor ticks every day
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,5*86400)
			self._tick_labels = [spiceypy.timout(t,'DOY') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(86400)
		elif self._sec_per_cm>(2*86400):
			# Ticks every 4 days, minor ticks every 12 hours
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,4*86400)
			self._tick_labels = [spiceypy.timout(t,'DOY') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(12*3600)
		elif self._sec_per_cm>86400:
			# Ticks every 2 days, minor ticks every 12 hours
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,2*86400)
			self._tick_labels = [spiceypy.timout(t,'DOY') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(12*3600)
		elif self._sec_per_cm>21600:
			# Ticks every 24 hours, minor ticks every 3 hours
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,86400)
			self._tick_labels = [spiceypy.timout(t,'DOY') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(10800)
		elif self._sec_per_cm>3600:
			# Ticks every 3 hours, minor ticks every 30 minutes
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,3*3600)
			self._tick_labels = [spiceypy.timout(t,'DOY HR:MN') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(1800)
		elif self._sec_per_cm>1800:
			# Ticks every hour, minor ticks every 10 minutes
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,3600)
			self._tick_labels = [spiceypy.timout(t,'DOY HR:MN') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(600)
		else:
			# Ticks every 10 minutes
			tick_start_time = self.round_up_day(self._start_time)
			self._ticks = np.arange(tick_start_time,self._end_time,600)
			self._tick_labels = [spiceypy.timout(t,'HR:MN') for t in self._ticks]
			self._minor_locator = matplotlib.ticker.MultipleLocator(6)

	def round_up_day(self, t):
		# Take a timestamp and round it up to the nearest day and return
		# a new timestamp for the start of the next day.
		jd_str = spiceypy.et2utc(t,'j',0)[3:]+'5'
		return spiceypy.str2et('JD '+jd_str)+0.1

	def set_x(self):
		for l in self._panel_labels:
			self._fig[l].ax.set_xlim([self._start_time,self._end_time])
			self._fig[l].ax.set_xticks(self._ticks)
			if l==self._panel_bottom:
				self._fig[l].ax.set_xticklabels(self._tick_labels)
			else:
				self._fig[l].ax.set_xticklabels([])
			self._fig[l].ax.xaxis.set_minor_locator(self._minor_locator)
