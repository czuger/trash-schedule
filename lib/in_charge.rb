class InCharge

  LIC_FILENAME = 'data/last_in_charge.txt'

  attr_reader :current_in_charge, :next_in_charge, :last_in_charge

  def read
    @in_charges = File.open('data/in_charges.txt','r').readlines.map{ |e| e.strip }

    if File.exists?(LIC_FILENAME)
      last_in_charge = File.open(LIC_FILENAME,'r').read.strip
      last_in_charge_position = @in_charges.index(last_in_charge)
      current_in_charge_position = increase_current_in_charge_position(last_in_charge_position)
      @current_in_charge = @in_charges[current_in_charge_position]
    else
      current_in_charge_position = 0
      @current_in_charge = @in_charges.first
    end

    next_in_charge_position = increase_current_in_charge_position(current_in_charge_position)
    @next_in_charge = @in_charges[next_in_charge_position]
    last_in_charge_position = increase_current_in_charge_position(next_in_charge_position)
    @last_in_charge = @in_charges[last_in_charge_position]

    self
  end

  def save
    File.open(LIC_FILENAME,'w').write(@current_in_charge)
  end

  private

  def increase_current_in_charge_position(position)
    position += 1
    return position if @in_charges[position]
    0
  end

end