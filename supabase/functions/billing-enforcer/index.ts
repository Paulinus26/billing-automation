import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // 1. Extract the customer_id from the incoming request
  const { customer_id } = await req.json()

  // 2. Initialize the Supabase Client
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  // 3. Query the 'billing_status' table we created in the SQL Editor
  const { data, error } = await supabase
    .from('billing_status')
    .select('is_active, current_usage, usage_limit')
    .eq('customer_id', customer_id)
    .single()

  // Handle errors (like if the user doesn't exist)
  if (error || !data) {
    return new Response(JSON.stringify({ error: "User not found in database" }), { 
      headers: { "Content-Type": "application/json" }, 
      status: 404 
    })
  }

  // 4. THE LOGIC: Is the account active AND is usage below the limit?
  const isAuthorized = data.is_active && data.current_usage < data.usage_limit

  // 5. Return the result
  return new Response(
    JSON.stringify({ 
      authorized: isAuthorized,
      usage: `${data.current_usage}/${data.usage_limit}`,
      status: data.is_active ? "Account Active" : "Account Suspended",
      message: isAuthorized ? "Access Granted" : "Access Denied: Usage Limit Exceeded"
    }),
    { headers: { "Content-Type": "application/json" } }
  )
})