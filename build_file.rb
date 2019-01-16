require 'pp'
require 'date'

class BuildFile

  def initialize
    read_dates
    read_in_charge
  end

  private

  def read_dates
    @dates = File.open('dates.txt','r').readlines
    @dates.shift
    @dates = @dates.map{ |e| read_date_line( e ) }
  end

  def read_date_line(date_line)
    dates_data = date_line.strip.split.map{ |e| build_date(e) }
    { jaune: dates_data[0], bleue: dates_data[1] }
  end

  def build_date(date_string)
    e = date_string.split('/')
    DateTime.new(e[2].to_i + 2000, e[1].to_i, e[0].to_i)
  end

  def read_in_charge
    @in_charge = File.open('responsables.txt','r').readlines.map{ |e| e.strip }
  end

end

pp BuildFile.new