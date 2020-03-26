require 'pp'
require 'date'
require 'odf-report'
require 'i18n'
require 'yaml'
require 'ostruct'

require_relative 'lib/dates_handler'
require_relative 'lib/in_charge'

class BuildFile

  def initialize
    # @dates = DatesHandler.new.read
    # @in_charge = InCharge.new.read

    @in_charge = [ 'Etage 2 - Kruger', 'Etage 1 - Liebhard-Zuger', 'Etage 0 - Holder' ]
    @exceptions = {
      Date.new( 2020, 4, 6 ) => Date.new( 2020, 4, 4 ),
      Date.new( 2020, 4, 9 ) => Date.new( 2020, 4, 8 ),
      Date.new( 2020, 4, 13 ) => Date.new( 2020, 4, 14 ),
      Date.new( 2020, 4, 16 ) => Date.new( 2020, 4, 17 ),
      Date.new( 2020, 5, 21 ) => Date.new( 2020, 5, 22 ),
      Date.new( 2020, 6, 1 ) => Date.new( 2020, 6, 2 ),
      Date.new( 2020, 6, 4 ) => Date.new( 2020, 6, 5 ),
      Date.new( 2020, 7, 16 ) => Date.new( 2020, 7, 17 ),
      Date.new( 2020, 11, 12 ) => Date.new( 2020, 11, 13 ),
      Date.new( 2020, 12, 21 ) => Date.new( 2020, 12, 19 ),
      Date.new( 2020, 12, 24 ) => Date.new( 2020, 12, 23 )
    }
  end

  def go
    report = ODFReport::Report.new('modeles/Courier model poubelles.odt') do |r|

      final_report = []

      monday = Date.new( 2020, 3, 30 )
      1.upto( 40 ).each do
        tuesday = monday + 3

        print_monday = monday
        if @exceptions[print_monday]
          print_monday = @exceptions[print_monday]
        end
        print_tuesday = tuesday

        p print_tuesday

        if @exceptions[print_tuesday]
          print_tuesday = @exceptions[print_tuesday]
        end

        final_report << OpenStruct.new( date: print_tuesday,
                                        blue: I18n.l(print_tuesday, format: '%A, %-d %B').humanize + (@exceptions[tuesday] ? ' *' : ''),
                                        yellow:  I18n.l(print_monday, format: '%A, %-d %B').humanize + (@exceptions[monday] ? ' *' : ''),
                                        responsable: get_floor )

        monday = monday + 7
      end

      r.add_table('Tableau1', final_report, :header=>true) do |t|
        t.add_column(:responsable)
        t.add_column(:yellow)
        t.add_column(:blue)
      end
    end

    report.generate('print/Planning sortie poubelles.odt')
    # @in_charge.save
  end

  def get_floor
    f = @in_charge.shift
    @in_charge << f
    f
  end

end

I18n.load_path = Dir['config/*.yml']
I18n.backend.load_translations
I18n.available_locales = [:fr]
I18n.locale = :fr

BuildFile.new.go