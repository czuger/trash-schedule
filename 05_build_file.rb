require 'pp'
require 'date'
require 'odf-report'
require 'i18n'

require_relative 'lib/dates_handler'
require_relative 'lib/in_charge'

class BuildFile

  def initialize
    @dates = DatesHandler.new.read
    @in_charge = InCharge.new.read
  end

  def go
    report = ODFReport::Report.new('data/Courier model poubelles.odt') do |r|

      r.add_table('TABLE_1', @list_of_itens, :header=>true) do |t|
        t.add_column(:item_id, :id)
        t.add_column(:description) { |item| "==> #{item.description}" }
      end


      r.add_field :date_jaune_out, @dates.out_j
      r.add_field :date_jaune_in, @dates.in_j
      r.add_field :date_bleue_out, @dates.out_b
      r.add_field :date_bleue_in, @dates.in_b

      r.add_field :resp_semaine_1, @in_charge.current_in_charge
      r.add_field :resp_semaine_2, @in_charge.next_in_charge
      r.add_field :resp_semaine_3, @in_charge.last_in_charge

      r.add_field :next_week, @dates.next_week_number
      r.add_field :last_week, @dates.last_week_number
    end

    report.generate('file.odt')
    @in_charge.save
  end

end

I18n.load_path = Dir['config/*.yml']
I18n.backend.load_translations
I18n.available_locales = [:fr]
I18n.locale = :fr

BuildFile.new.go