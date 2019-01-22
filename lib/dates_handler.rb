require 'active_support/all'

class DatesHandler

  attr_reader :current_week_number, :next_week_number, :last_week_number, :out_j, :out_b, :in_j, :in_b

  def read
    @dates = File.open('data/dates.txt','r').readlines
    @dates.shift
    @dates = @dates.map{ |e| read_date_line( e ) }.flatten
    # pp @dates
    set_current_date
    self
  end

  private

  def set_current_date
    while((@dates.first[:type] == :bleue && @dates.first[:date] <= DateTime.now) || @dates.first[:type] == :jaune)
      @dates.shift
    end

    @blue_date = @dates.shift
    @yellow_date = @dates.first

    @current_week_number = DateTime.now.cweek
    @next_week_number = DateTime.now.next_day(7).cweek
    @last_week_number = DateTime.now.next_day(14).cweek

    @out_j = format_date(@yellow_date[:date] - (1/24.0)*6)
    @in_j = format_date(@yellow_date[:date] + (1/24.0)*10)
    @out_b = format_date(@blue_date[:date] - (1/24.0)*6)
    @in_b = format_date(@blue_date[:date] + (1/24.0)*10)
  end

  def format_date(date)
    # date.strftime('%A, %-d %B à partir de %H heure')
    I18n.l(date, format: '%A, %-d %B à partir de %H heure')
  end

  def read_date_line(date_line)
    dates_data = date_line.strip.split.map{ |e| build_date(e) }
    [ {type: :jaune, date: dates_data[0], day_before: dates_data[0] - (1/24.0)*6}, {type: :bleue, date: dates_data[1]} ]
  end

  def build_date(date_string)
    e = date_string.split('/')
    DateTime.new(e[2].to_i + 2000, e[1].to_i, e[0].to_i)
  end

end