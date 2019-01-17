require 'pp'
require 'date'
require 'odf-report'

class BuildFile

  def initialize
    read_dates
    read_in_charge
  end

  def go
    report = ODFReport::Report.new('Courier model poubelles.odt') do |r|
      dw = dates_for_current_week

      r.add_field :date_jaune_out, dw.shift
      r.add_field :date_jaune_in, dw.shift
      r.add_field :date_bleue_out, dw.shift
      r.add_field :date_bleue_in, dw.shift

      r.add_field :resp_semaine_1, @in_charge[0]
      r.add_field :resp_semaine_2, @in_charge[1]
      r.add_field :resp_semaine_3, @in_charge[2]
    end
    report.generate('file.odt')
  end

  private

  def dates_for_current_week
    out_j = format_date(@current_dates[:jaune] - (1/24.0)*6)
    in_j = format_date(@current_dates[:jaune] + (1/24.0)*10)
    out_b = format_date(@current_dates[:bleue] - (1/24.0)*6)
    in_b = format_date(@current_dates[:bleue] + (1/24.0)*10)
    [out_j, in_j, out_b, in_b]
  end

  def format_date(date)
    date.strftime('%A, %-d %B à partir de %H heure')
  end

  def read_dates
    @dates = File.open('dates.txt','r').readlines
    @dates.shift
    @dates = @dates.map{ |e| read_date_line( e ) }
    @current_dates = @dates.first
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

pp BuildFile.new.go