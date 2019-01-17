class DatesHandler

  def read
    @dates = File.open('data/dates.txt','r').readlines
    @dates.shift
    @dates = @dates.map{ |e| read_date_line( e ) }
    set_current_date
    self
  end

  def dates_for_current_week
    out_j = format_date(@current_dates[:jaune] - (1/24.0)*6)
    in_j = format_date(@current_dates[:jaune] + (1/24.0)*10)
    out_b = format_date(@current_dates[:bleue] - (1/24.0)*6)
    in_b = format_date(@current_dates[:bleue] + (1/24.0)*10)
    [out_j, in_j, out_b, in_b]
  end

  private

  def set_current_date
    while(@dates.first[:jaune] < DateTime.now)
      @dates.shift
    end
    @current_dates = @dates.first
  end

  def format_date(date)
    # date.strftime('%A, %-d %B à partir de %H heure')
    I18n.l(date, format: '%A, %-d %B à partir de %H heure')
  end

  def read_date_line(date_line)
    dates_data = date_line.strip.split.map{ |e| build_date(e) }
    { jaune: dates_data[0], bleue: dates_data[1] }
  end

  def build_date(date_string)
    e = date_string.split('/')
    DateTime.new(e[2].to_i + 2000, e[1].to_i, e[0].to_i)
  end

end