# load the gem
require 'ruby_dlrnapi'

# hard code to pike
#api_client = RubyDlrnapi::ApiClient.new("https://trunk.rdoproject.org/api-centos-pike")

api_client = RubyDlrnapi::ApiClient.new()
api_client.config.host = "https://trunk.rdoproject.org/api-centos-pike"
api_instance = RubyDlrnapi::DefaultApi.new(api_client)

params = RubyDlrnapi::Params5.new # Params5 | The JSON params to post


begin
  result = api_instance.api_promotions_get(params)
  p result
rescue RubyDlrnapi::ApiError => e
  puts "Exception when calling DefaultApi->api_promotions_get: #{e}"
end