#require 'xmlsimple'
#require 'pathname'
  
  
#require 'nokogiri'
require 'open-uri'
require 'pp'
#require 'meta_search' 
  
class SongsController < ApplicationController
   
  def index
    #pp 
    @search_str = String.new#
    if params[:search_box_wdyn] == nil
      @songs = []
      @search_str = 'insert search string'
    else
      @search_str = params[:search_box_wdyn]
      search_qstr = '%'+params[:search_box_wdyn]+'%'
      @songs = Song.all(:conditions => [' artist like ? or album like ? or title like ? or location like ? ',search_qstr,search_qstr,search_qstr,search_qstr])
      #pp @songs
    end
  
  end
  def search
    #pp 
    @search_str = String.new#
    if params[:search_box_wdyn] == nil
      @songs = []
      @search_str = 'insert search string'
    else
      @search_str = params[:search_box_wdyn]
      search_qstr = '%'+params[:search_box_wdyn]+'%'
      @songs = Song.all(:conditions => [' artist like ? or album like ? or title like ? or location like ? ',search_qstr,search_qstr,search_qstr,search_qstr])
      #pp @songs
    end
    

    #render :layout => 'weshouldshareit' 
  end
  def search_details
    @search_str = String.new
    @artist = String.new
    @album = String.new
    @title = String.new
    @location = String.new
    @songs = []
    if params[:artist] != nil
      artist_qstr = '%'+params[:artist]+'%'
      @artist = params[:artist]
    end
    if params[:album] != nil
      album_qstr = '%'+params[:album]+'%'
      @album = params[:album]
    end
    if params[:title] != nil
      title_qstr = '%'+params[:title]+'%'
      @title = params[:title]
    end
    if params[:location] != nil
      location_qstr = '%'+params[:location]+'%'
      @location = params[:location]
    end
    if artist_qstr != nil or album_qstr != nil or title_qstr != nil or location_qstr != nil 
      @songs = Song.all(:conditions => [' artist like ? and album like ? and title like ?  and location like ? ',artist_qstr,album_qstr,title_qstr,location_qstr])
      #pp @songs
    end
    
  end

  def meta_search
    @search = Song.search(params[:search])
    @songs = @search.all
  end

end